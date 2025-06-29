from django.contrib import admin
from .models import SolicitudPoda

@admin.register(SolicitudPoda)
class SolicitudPodaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'motivo_poda', 'fecha_creacion', 'estatus')
    list_filter = ('estatus', 'motivo_poda', 'ubicacion_poda', 'alcaldia_poda')
    search_fields = ('usuario__email', 'calle_poda', 'colonia_poda', 'cp_poda')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'estatus', 'fecha_creacion')
        }),
        ('Ubicación', {
            'fields': ('latitud', 'longitud', 'calle_poda', 'numero_ext_poda', 
                      'numero_int_poda', 'colonia_poda', 'alcaldia_poda', 
                      'cp_poda', 'ubicacion_poda', 'referencias_poda')
        }),
        ('Detalles de Poda', {
            'fields': ('motivo_poda', 'foto_poda')
        }),
    )