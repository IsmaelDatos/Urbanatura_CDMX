# Etapa de construcción
FROM python:3.9-slim as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY COPY requirements.txt .

RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Etapa de producción
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

WORKDIR /app
COPY backend .  # Copia todo el contenido de backend a /app

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=urbanatura_cdmx.settings \
    PORT=8000

RUN python manage.py collectstatic --noinput

EXPOSE $PORT
CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]