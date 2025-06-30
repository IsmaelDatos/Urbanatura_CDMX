from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings

User = get_user_model()

class SolicitudDerribo(models.Model):
    class MotivoDerribo(models.TextChoices):
        RIESGO = 'riesgo', _('Riesgo de caída')
        ENFERMEDAD = 'enfermedad', _('Enfermedad irreversible')
        CONSTRUCCION = 'construccion', _('Para construcción')
        OBSTRUCCION = 'obstruccion', _('Obstrucción grave')
        OTRO = 'otro', _('Otro motivo')

    class Ubicacion(models.TextChoices):
        BANQUETA = 'banqueta', _('Banqueta')
        CAMELLON = 'camellon', _('Camellón')
        PROPIEDAD_PRIVADA = 'propiedad_privada', _('Propiedad privada')
        AREA_PUBLICA = 'area_publica', _('Área pública')
        
    class Estatus(models.TextChoices):
        PENDIENTE = 'pendiente', _('Pendiente')
        APROBADA = 'aprobada', _('Aprobada')
        RECHAZADA = 'rechazada', _('Rechazada')
        REQUIERE_APROBACION = 'requiere_aprobacion', _('Requiere aprobación especial')

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitudes_derribo'
    )

    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

    cp_derribo = models.CharField('Código postal', max_length=5)
    alcaldia_derribo = models.CharField('Alcaldía', max_length=60)
    colonia_derribo = models.CharField('Colonia', max_length=120)
    calle_derribo = models.CharField('Calle', max_length=120)
    numero_ext_derribo = models.CharField('Número exterior', max_length=10)
    numero_int_derribo = models.CharField('Número interior', max_length=10, blank=True, null=True)

    motivo_derribo = models.CharField(max_length=20, choices=MotivoDerribo.choices)
    ubicacion_derribo = models.CharField(max_length=20, choices=Ubicacion.choices)
    foto_derribo = models.TextField(verbose_name='Imagen del árbol en Base64')
    justificacion_derribo = models.TextField('Justificación del derribo')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=20, choices=Estatus.choices, default=Estatus.PENDIENTE)

    class Meta:
        verbose_name = 'Solicitud de Derribo'
        verbose_name_plural = 'Solicitudes de Derribo'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Solicitud #{self.pk} por {self.usuario.username} – {self.calle_derribo}, {self.colonia_derribo}"