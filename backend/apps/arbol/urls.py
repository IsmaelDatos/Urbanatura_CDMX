from django.urls import path
from . import views
from .views import (
    home_ciudadano,
    home_institucion
)

app_name = 'arbol' 

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agregar/', views.agregar_arbol, name='agregar_arbol'),
    path('lista/', views.lista_arboles, name='lista_arboles'),
    path('modificar/<int:id>/', views.modificar_arbol, name='modificar_arbol'),
    path('eliminar/<int:id>/', views.eliminar_arbol, name='eliminar_arbol'),
    path('documentacion/', views.documentacion, name='documentacion'),
    path('informacion_empresa/', views.informacion_empresa, name='informacion_empresa'),
    path('datos-mapa/', views.datos_mapa, name='datos_mapa'),
    path('home-ciudadano/', home_ciudadano, name='home_ciudadano'),
    path('home-institucion/', home_institucion, name='home_institucion'),
]