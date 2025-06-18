# Etapa de construcción
FROM python:3.9-slim as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# Etapa de producción
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000

COPY --from=builder /install /usr/local
COPY --from=builder /app/backend /app
COPY backend/urbanatura_cdmx/templates backend/urbanatura_cdmx/templates

# Copiar archivos estáticos a la raíz /static del contenedor
COPY backend/urbanatura_cdmx/static /static

WORKDIR /app

# Crear directorios media si es necesario
RUN mkdir -p /app/media

EXPOSE $PORT

CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]
