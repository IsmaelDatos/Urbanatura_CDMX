from django.urls import path
from .views import CrearSolicitudPodaView, ListaSolicitudesPodaView

app_name = 'poda'

urlpatterns = [
    path('solicitar/', CrearSolicitudPodaView.as_view(), name='solicitar'),
    path('mis-solicitudes/', ListaSolicitudesPodaView.as_view(), name='lista'),
]