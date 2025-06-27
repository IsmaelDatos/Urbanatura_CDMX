from django.urls import path
from . import views
from .views import register_ciudadano, register_institucion, user_login, user_logout, edit_ciudadano, edit_institucion
app_name = 'usuarios'
urlpatterns = [
    path('registrar/ciudadano/', register_ciudadano, name='registrar_ciudadano'),
    path('registrar/institucion/', register_institucion, name='registrar_institucion'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('editar/ciudadano/', edit_ciudadano, name='edit_ciudadano'),
    path('editar/institucion/', edit_institucion, name='edit_institucion'),
]