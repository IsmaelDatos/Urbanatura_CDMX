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

FROM python:3.9-slim
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000

# 1. Copiar dependencias instaladas
COPY --from=builder /install /usr/local

# 2. Copiar todo el backend (incluyendo código Python)
COPY --from=builder /app/backend /app

# 3. Copiar archivos estáticos a ubicación compatible con WhiteNoise
COPY --from=builder /app/backend/urbanatura_cdmx/static /app/staticfiles
COPY --from=builder /app/backend/urbanatura_cdmx/static /app/backend/urbanatura_cdmx/static

# 4. Crear directorios necesarios
RUN mkdir -p /app/media /app/staticfiles

# 5. Configurar permisos (importante para Fly.io)
RUN chmod -R a+rwx /app/media /app/staticfiles

WORKDIR /app
EXPOSE $PORT
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]

# FROM python:3.9-slim as builder
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app
# COPY . .

# RUN pip install --upgrade pip && \
#     pip install --prefix=/install --no-cache-dir -r requirements.txt

# FROM python:3.9-slim
# RUN apt-get update && apt-get install -y \
#     libpq5 \
#     && rm -rf /var/lib/apt/lists/*
# ENV PYTHONUNBUFFERED=1 \
#     DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
#     PORT=8000
# COPY --from=builder /install /usr/local
# COPY --from=builder /app/backend /app
# COPY backend/urbanatura_cdmx/templates backend/urbanatura_cdmx/templates
# COPY backend/urbanatura_cdmx/static /static
# WORKDIR /app
# RUN mkdir -p /app/media
# EXPOSE $PORT
# CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]


