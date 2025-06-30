from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings

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
        
    class Estatus(models.TextChoices):
        PENDIENTE = 'pendiente', _('Pendiente')
        APROBADA = 'aprobada', _('Aprobada')
        RECHAZADA = 'rechazada', _('Rechazada')
        REQUIERE_INSPECCION = 'requiere_inspeccion', _('Requiere inspección')

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitudes_traslado'
    )

    # Coordenadas de ubicación actual
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

    # Ubicación actual
    cp_actual_traslado = models.CharField('Código postal actual', max_length=5)
    alcaldia_actual_traslado = models.CharField('Alcaldía actual', max_length=60)
    colonia_actual_traslado = models.CharField('Colonia actual', max_length=120)
    calle_actual_traslado = models.CharField('Calle actual', max_length=120)
    numero_ext_actual_traslado = models.CharField('Número exterior actual', max_length=10)
    numero_int_actual_traslado = models.CharField('Número interior actual', max_length=10, blank=True, null=True)

    # Ubicación nueva (opcional)
    calle_nueva_traslado = models.CharField('Calle nueva', max_length=120, blank=True, null=True)
    numero_ext_nueva_traslado = models.CharField('Número exterior nuevo', max_length=10, blank=True, null=True)
    alcaldia_nueva_traslado = models.CharField('Alcaldía nueva', max_length=60, blank=True, null=True)
    colonia_nueva_traslado = models.CharField('Colonia nueva', max_length=120, blank=True, null=True)

    # Información del traslado
    motivo_traslado = models.CharField(max_length=20, choices=MotivoTraslado.choices)
    ubicacion_actual_traslado = models.CharField(max_length=20, choices=UbicacionActual.choices)
    foto_traslado = models.TextField(verbose_name='Imagen del árbol en Base64')
    info_adicional_traslado = models.TextField('Información adicional')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=20, choices=Estatus.choices, default=Estatus.PENDIENTE)

    class Meta:
        verbose_name = 'Solicitud de Traslado'
        verbose_name_plural = 'Solicitudes de Traslado'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Solicitud #{self.pk} por {self.usuario.username} – {self.calle_actual_traslado}"

    def tiene_ubicacion_nueva(self):
        return bool(self.calle_nueva_traslado)