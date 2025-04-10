from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'tipo_usuario', 'is_staff')
    search_fields = ('email', 'first_name', 'nombre_institucion')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'primer_apellido', 'segundo_apellido', 'nombre_institucion', 'rfc', 'tipo_usuario', 'telefono')}),
        ('Dirección', {'fields': ('calle', 'num_ext', 'num_int', 'entidad_federativa', 'municipio', 'codigo_postal', 'referencias')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(Usuario, UsuarioAdmin)