from django.contrib import admin
from .models import Arbol

@admin.register(Arbol)
class ArbolAdmin(admin.ModelAdmin):
    list_display = ('nombre_comun', 'nombre_cientifico', 'colonia', 'calle', 'altura', 'condicion_general')
    list_filter = ('condicion_general', 'ubicacion', 'municipio_alcaldia')
    search_fields = ('nombre_comun', 'nombre_cientifico', 'colonia', 'calle', 'codigo_postal')
    readonly_fields = ('fecha_registro',)
    fieldsets = (
        ('Identificación', {
            'fields': ('nombre_comun', 'nombre_cientifico', 'numero_arbol')
        }),
        ('Ubicación', {
            'fields': ('entidad_federativa', 'municipio_alcaldia', 'colonia',
                      'calle', 'num_ext', 'num_int', 'codigo_postal',
                      'ubicacion', 'ubicacion_otro', 'latitud', 'longitud')
        }),
        ('Características Físicas', {
            'fields': ('altura', 'diametro_tronco', 'diametro_copa',
                      'inclinacion_tronco', 'estructura_general',
                      'condicion_general', 'inclinacion_terreno')
        }),
        ('Fotografías', {
            'fields': ('foto1', 'foto2', 'foto3', 'foto4', 'foto5')
        }),
    )