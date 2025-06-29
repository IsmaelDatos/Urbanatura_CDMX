from django.contrib import admin
from .models import SolicitudTraslado

@admin.register(SolicitudTraslado)
class SolicitudTrasladoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'motivo_traslado', 'fecha_creacion', 'estatus', 'tiene_ubicacion_nueva')
    list_filter = ('estatus', 'motivo_traslado', 'ubicacion_actual_traslado')
    search_fields = ('usuario__email', 'calle_actual_traslado', 'colonia_actual_traslado')
    readonly_fields = ('fecha_creacion', 'tiene_ubicacion_nueva')
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'estatus', 'fecha_creacion')
        }),
        ('Ubicación Actual', {
            'fields': ('latitud', 'longitud', 'ubicacion_actual_traslado',
                      'calle_actual_traslado', 'numero_ext_actual_traslado',
                      'numero_int_actual_traslado', 'colonia_actual_traslado',
                      'alcaldia_actual_traslado', 'cp_actual_traslado')
        }),
        ('Ubicación Nueva (opcional)', {
            'fields': ('calle_nueva_traslado', 'numero_ext_nueva_traslado',
                      'alcaldia_nueva_traslado', 'colonia_nueva_traslado')
        }),
        ('Detalles del Traslado', {
            'fields': ('motivo_traslado', 'info_adicional_traslado', 'foto_traslado')
        }),
    )