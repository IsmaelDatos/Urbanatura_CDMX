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

# Configura el entorno Python correctamente
ENV PYTHONPATH=/app

COPY --from=builder /install /usr/local
COPY --from=builder /app/backend /app

# Crea directorios necesarios
RUN mkdir -p /app/staticfiles && \
    mkdir -p /app/urbanatura_cdmx/static

# Configuración de entorno
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000

WORKDIR /app

# Verifica que el módulo sea importable
RUN python -c "import urbanatura_cdmx" || echo "Error al importar"

EXPOSE $PORT
CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]