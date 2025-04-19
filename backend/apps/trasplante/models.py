from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class SolicitudTraslado(models.Model):
    class MotivoTraslado(models.TextChoices):
        CONSERVACION = 'conservacion', _('Conservación del árbol')
        CONSTRUCCION = 'construccion', _('Obra de construcción')
        MEJOR_UBICACION = 'mejor_ubicacion', _('Mejor ubicación para su desarrollo')
        RIESGO = 'riesgo', _('Por riesgo en ubicación actual')

    class UbicacionActual(models.TextChoices):
        BANQUETA = 'banqueta', _('Banqueta')
        CAMELLON = 'camellon', _('Camellón')
        JARDIN_PRIVADO = 'jardin_privado', _('Jardín privado')
        AREA_VERDE = 'area_verde', _('Área verde pública')

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_traslado')
    motivo_traslado = models.CharField(max_length=20, choices=MotivoTraslado.choices)
    foto_traslado = models.ImageField(upload_to='traslado/')
    ubicacion_actual_traslado = models.CharField(max_length=20, choices=UbicacionActual.choices)
    calle_actual_traslado = models.CharField(max_length=100)
    numero_ext_actual_traslado = models.CharField(max_length=10)
    numero_int_actual_traslado = models.CharField(max_length=10, blank=True, null=True)
    alcaldia_actual_traslado = models.CharField(max_length=50)
    colonia_actual_traslado = models.CharField(max_length=50)
    cp_actual_traslado = models.CharField(max_length=5)
    calle_nueva_traslado = models.CharField(max_length=100, blank=True, null=True)
    numero_ext_nueva_traslado = models.CharField(max_length=10, blank=True, null=True)
    alcaldia_nueva_traslado = models.CharField(max_length=50, blank=True, null=True)
    colonia_nueva_traslado = models.CharField(max_length=50, blank=True, null=True)
    info_adicional_traslado = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=20, default='pendiente', 
                              choices=[('pendiente', 'Pendiente'), 
                                      ('aprobada', 'Aprobada'), 
                                      ('rechazada', 'Rechazada'),
                                      ('requiere_inspeccion', 'Requiere inspección')])

    class Meta:
        verbose_name = 'Solicitud de Traslado'
        verbose_name_plural = 'Solicitudes de Traslado'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Solicitud de traslado #{self.id} - {self.usuario.email}"

    def tiene_ubicacion_nueva(self):
        return bool(self.calle_nueva_traslado)