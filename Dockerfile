FROM python:3.9-slim as builder

WORKDIR /app
COPY . .

# Instalar dependencias del sistema y Python
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --user -r requirements.txt

FROM python:3.9-slim

# Dependencias de runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000 \
    PATH="/app/.local/bin:${PATH}"

# Copiar solo lo necesario desde el builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/backend /app

# Crear directorios y configurar permisos
RUN mkdir -p /app/staticfiles /app/media \
    && chmod -R a+rwx /app/media /app/staticfiles

WORKDIR /app

# Exponer puerto y comando de inicio
EXPOSE $PORT
CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]