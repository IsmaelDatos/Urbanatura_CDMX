from django.urls import path
from . import views

urlpatterns = [
    path('solicitar-poda/', views.solicitar_poda, name='solicitar_poda'),
]
