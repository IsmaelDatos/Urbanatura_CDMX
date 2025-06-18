# Etapa de construcción
FROM python:3.9-slim as builder

# 1. Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Configurar entorno Python
WORKDIR /app
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# 3. Instalar dependencias
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Etapa de producción ---
FROM python:3.9-slim

# 1. Copiar solo lo necesario desde la etapa de construcción
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/requirements.txt .

# 2. Configurar entorno
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000

# 3. Instalar dependencias de runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiar aplicación
COPY . .

# 5. Configurar usuario no root
RUN useradd -m myuser && \
    chown -R myuser:myuser /app && \
    mkdir -p /app/static && \
    chown myuser:myuser /app/static
USER myuser

# 6. Colectar archivos estáticos
RUN python manage.py collectstatic --noinput

# 7. Exponer puerto y ejecutar
EXPOSE $PORT
CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]