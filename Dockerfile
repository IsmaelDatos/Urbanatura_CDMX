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

# Configuración de entorno
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000

# Copia las dependencias instaladas
COPY --from=builder /install /usr/local

# Copia el proyecto (nota el cambio aquí)
COPY --from=builder /app/backend /app

WORKDIR /app

# Crea directorios necesarios
RUN mkdir -p /app/static && \
    mkdir -p /app/media

# Ejecuta collectstatic
RUN python manage.py collectstatic --noinput --clear

EXPOSE $PORT
CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]