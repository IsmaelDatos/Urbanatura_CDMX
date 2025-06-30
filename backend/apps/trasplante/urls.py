from django.urls import path
from .views import (
    CrearSolicitudTrasladoView,
    ListaSolicitudesTrasladoView,
    DetalleSolicitudTrasladoView
)

app_name = 'traslado'

urlpatterns = [
    path('solicitar/', CrearSolicitudTrasladoView.as_view(), name='solicitar'),
    path('mis-solicitudes/', ListaSolicitudesTrasladoView.as_view(), name='lista'),
    path('mis-solicitudes/<int:pk>/', DetalleSolicitudTrasladoView.as_view(), name='detalle'),
]