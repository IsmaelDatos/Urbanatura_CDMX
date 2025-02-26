from django.urls import path
from . import views
urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página de inicio
    path('agregar/', views.agregar_arbol, name='agregar_arbol'),
    path('lista/', views.lista_arboles, name='lista_arboles'),
    path('modificar/<int:id>/', views.modificar_arbol, name='modificar_arbol'),
    path('eliminar/<int:id>/', views.eliminar_arbol, name='eliminar_arbol'),
    path('documentacion/', views.documentacion, name='documentacion'),
    path('informacion_empresa/', views.informacion_empresa, name='informacion_empresa'),
]