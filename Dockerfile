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

# Copy from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/backend /app

# Create directories
RUN mkdir -p /app/static /app/media && \
    chmod -R a+rwx /app/media /app/static

WORKDIR /app

# Expose port
EXPOSE $PORT

# Health check (opcional pero recomendado)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Run command
CMD ["gunicorn", "urbanatura_cdmx.wsgi:application", "--bind", "0.0.0.0:8000"]