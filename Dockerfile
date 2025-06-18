FROM python:3.9-slim as builder

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias de Python primero (para aprovechar el cache de Docker)
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Fase de producción ---
FROM python:3.9-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000

# Copiar solo lo necesario desde la fase de builder
COPY --from=builder /root/.local /root/.local
COPY . /app

WORKDIR /app

# Asegurar que los scripts estén en PATH
ENV PATH=/root/.local/bin:$PATH

# Exponer el puerto que Fly.io usará
EXPOSE $PORT

# Comando para ejecutar la aplicación
CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]