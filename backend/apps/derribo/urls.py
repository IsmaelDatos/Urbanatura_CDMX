from django.urls import path
from .views import (
    CrearSolicitudDerriboView, 
    ListaSolicitudesDerriboView,
    DetalleSolicitudDerriboView
)

app_name = 'derribo'

urlpatterns = [
    path('solicitar/', CrearSolicitudDerriboView.as_view(), name='solicitar'),
    path('mis-solicitudes/', ListaSolicitudesDerriboView.as_view(), name='lista'),
    path('mis-solicitudes/<int:pk>/', DetalleSolicitudDerriboView.as_view(), name='detalle'),
]