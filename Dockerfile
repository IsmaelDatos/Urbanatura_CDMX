# Stage 1: Builder
FROM python:3.9-slim as builder

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Instalar dependencias Python
RUN pip install --user --no-cache-dir gunicorn==21.2.0 && \
    pip install --user --no-cache-dir -r requirements.txt

# Ejecutar collectstatic durante el build
RUN python manage.py collectstatic --noinput --clear

# Stage 2: Runtime
FROM python:3.9-slim

# Dependencias de tiempo de ejecución
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 curl && \  # Añadido curl para healthcheck
    rm -rf /var/lib/apt/lists/*

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000 \
    PATH="/root/.local/bin:${PATH}"

# Copiar desde el stage builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Configurar permisos
RUN chmod -R 755 /app/staticfiles && \  # Asegurar STATIC_ROOT
    chmod -R 755 /app/media && \
    find /app/staticfiles -type f -exec chmod 644 {} \; && \
    chown -R nobody:nogroup /app

WORKDIR /app

EXPOSE $PORT

# Healthcheck mejorado
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/static/css/base.css || exit 1

# Comando de inicio
CMD ["sh", "-c", "gunicorn urbanatura_cdmx.wsgi:application --bind 0.0.0.0:8000"]
