# Stage 1: Builder
FROM python:3.9-slim as builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos solo la carpeta backend para que manage.py esté dentro de /app/backend
COPY backend ./backend

# Instalar dependencias
RUN pip install --user --no-cache-dir gunicorn==21.2.0 && \
    pip install --user --no-cache-dir -r backend/requirements.txt

# Ejecutar collectstatic desde la ruta correcta
WORKDIR /app/backend
RUN python manage.py collectstatic --noinput --clear

# Stage 2: Runtime
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 curl && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000 \
    PATH="/root/.local/bin:${PATH}"

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

WORKDIR /app/backend

RUN chmod -R 755 /app/backend/staticfiles && \
    chmod -R 755 /app/backend/media && \
    find /app/backend/staticfiles -type f -exec chmod 644 {} \; && \
    chown -R nobody:nogroup /app

EXPOSE $PORT

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/static/css/base.css || exit 1

CMD ["sh", "-c", "gunicorn urbanatura_cdmx.wsgi:application --bind 0.0.0.0:8000"]
