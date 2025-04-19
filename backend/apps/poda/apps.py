# backend/apps/poda/apps.py
from django.apps import AppConfig

class PodaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'poda'
    verbose_name = 'Gestión de Podas'