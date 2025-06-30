# Stage 1: Builder
FROM python:3.9-slim as builder

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --user --no-cache-dir gunicorn==21.2.0 && \
    pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim

# Runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000 \
    PATH="/root/.local/bin:${PATH}"

# Copiar TODO el proyecto manteniendo la estructura exacta
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/backend /app

# Configuración ESPECÍFICA para tus estáticos (sin staticfiles)
RUN mkdir -p /app/media && \
    # Permisos explícitos solo para la carpeta static
    chmod -R 755 /app/urbanatura_cdmx/static && \
    # Asegurar que los archivos puedan ser leídos
    find /app/urbanatura_cdmx/static -type f -exec chmod 644 {} \; && \
    # Usuario correcto
    chown -R nobody:nogroup /app

WORKDIR /app

EXPOSE $PORT

# Health check mejorado
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/static/css/base.css || exit 1

# Comando de inicio optimizado
CMD ["sh", "-c", "gunicorn urbanatura_cdmx.wsgi:application --bind 0.0.0.0:8000"]