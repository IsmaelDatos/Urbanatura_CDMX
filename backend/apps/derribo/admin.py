from django.contrib import admin
from .models import SolicitudDerribo

@admin.register(SolicitudDerribo)
class SolicitudDerriboAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'motivo_derribo', 'fecha_creacion', 'estatus')
    list_filter = ('estatus', 'motivo_derribo', 'ubicacion_derribo', 'alcaldia_derribo')
    search_fields = ('usuario__email', 'calle_derribo', 'colonia_derribo', 'cp_derribo')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'estatus', 'fecha_creacion')
        }),
        ('Ubicación', {
            'fields': ('latitud', 'longitud', 'calle_derribo', 'numero_ext_derribo', 
                      'numero_int_derribo', 'colonia_derribo', 'alcaldia_derribo', 
                      'cp_derribo', 'ubicacion_derribo')
        }),
        ('Detalles del Derribo', {
            'fields': ('motivo_derribo', 'justificacion_derribo', 'foto_derribo')
        }),
    )