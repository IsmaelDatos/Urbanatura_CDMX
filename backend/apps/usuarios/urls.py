from django.urls import path
from . import views
from .views import register_ciudadano, register_institucion, user_login, user_logout, edit_ciudadano, edit_institucion
app_name = 'usuarios'
urlpatterns = [
    path('registrar/ciudadano/', views.register_ciudadano, name='registrar_ciudadano'),
    path('registrar/institucion/', views.register_institucion, name='registrar_institucion'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('editar/ciudadano/', views.edit_ciudadano, name='edit_ciudadano'),
    path('editar/institucion/', views.edit_institucion, name='edit_institucion'),
    path('home/ciudadano/', views.home_ciudadano, name='home_ciudadano'),
    path('home/institucion/', views.home_institucion, name='home_institucion'),
]