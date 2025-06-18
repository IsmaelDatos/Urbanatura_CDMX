#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Collect static files (usando la nueva ubicación)
python manage.py collectstatic --noinput --clear