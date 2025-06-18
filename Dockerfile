# Etapa de construcción
FROM python:3.9-slim as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Actualiza pip e instala dependencias
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# Etapa de producción
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copia las dependencias instaladas
COPY --from=builder /install /usr/local

WORKDIR /app
COPY ./backend .

# Crea directorios necesarios y recolecta archivos estáticos
RUN mkdir -p /app/staticfiles && \
    mkdir -p /app/urbanatura_cdmx/static/root && \
    python manage.py collectstatic --noinput

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000 \
    DEBUG=False

EXPOSE $PORT
CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]