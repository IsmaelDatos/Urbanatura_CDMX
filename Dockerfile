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

WORKDIR /app

# Crear directorios media y static si es necesario
RUN mkdir -p /app/media /app/backend/urbanatura_cdmx/static

# Copiar archivos estáticos a la ruta correcta en el contenedor
COPY backend/urbanatura_cdmx/static backend/urbanatura_cdmx/static

EXPOSE $PORT

CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]
