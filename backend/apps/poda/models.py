from django.db import models

class SolicitudPoda(models.Model):
    MOTIVOS_PODA = [
        ('crecimiento_desbalanceado', 'Crecimiento desbalanceado (Copa irregular que podría causar riesgo)'),
        ('interferencia_cables', 'Interferencia con cables de electricidad o telecomunicaciones'),
        ('obstruccion_paso', 'Obstrucción del paso peatonal o vehicular'),
        ('bloqueo_luminarias', 'Bloqueo de luminarias o señales de tránsito'),
        ('riesgo_caida_ramas', 'Riesgo de caída de ramas sobre espacios públicos o privados'),
        ('arbol_gran_altura', 'Árbol de gran altura que representa riesgo de desplome parcial'),
        ('ubicacion_inadecuada', 'Ubicación inadecuada (banqueta angosta, bajo un puente, interfiriendo con construcciones privadas o públicas)')
    ]
    
    UBICACIONES = [
        ('banqueta', 'Banqueta'),
        ('camellon', 'Camellón'),
        ('glorieta', 'Glorieta'),
        ('parque', 'Parque'),
        ('arriate', 'Arriate'),
        ('plaza', 'Plaza'),
        ('propiedad_privada', 'Propiedad privada'),
        ('obra_civil', 'Obra civil'),
        ('otro', 'Otro')
    ]
    
    motivo_poda = models.CharField(max_length=50, choices=MOTIVOS_PODA)
    foto = models.ImageField(upload_to='solicitudes_poda/')
    ubicacion = models.CharField(max_length=50, choices=UBICACIONES)
    calle = models.CharField(max_length=255)
    num_ext = models.CharField(max_length=20)
    num_int = models.CharField(max_length=20, blank=True, null=True)
    entidad_federativa = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    referencias = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'Solicitud de poda en {self.calle}, {self.municipio}'
