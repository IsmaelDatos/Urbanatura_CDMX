from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings
User = get_user_model()

class SolicitudPoda(models.Model):
    class MotivoPoda(models.TextChoices):
        MANTENIMIENTO   = 'mantenimiento',   'Mantenimiento preventivo'
        SEGURIDAD       = 'seguridad',       'Seguridad (ramas peligrosas)'
        SALUD           = 'salud',           'Salud del árbol'
        INTERFERENCIA   = 'interferencia',   'Interferencia con infraestructura'

    class UbicacionArbol(models.TextChoices):
        BANQUETA            = 'banqueta',           'Banqueta'
        CAMELLON            = 'camellon',           'Camellón'
        GLORIETA            = 'glorieta',           'Glorieta'
        PARQUE              = 'parque',             'Parque'
        ARRIATE             = 'arriate',            'Arriate'
        PLAZA               = 'plaza',              'Plaza'
        PROPIEDAD_PRIVADA   = 'propiedad_privada',  'Propiedad privada'

    class Estatus(models.TextChoices):
        PENDIENTE  = 'pendiente', 'Pendiente'
        APROBADA   = 'aprobada', 'Aprobada'
        RECHAZADA  = 'rechazada', 'Rechazada'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitudes_poda'
    )

    latitud  = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

    cp_poda         = models.CharField('Código postal', max_length=5)
    alcaldia_poda   = models.CharField('Alcaldía', max_length=60)
    colonia_poda    = models.CharField('Colonia', max_length=120)
    calle_poda      = models.CharField('Calle', max_length=120)
    numero_ext_poda = models.CharField('Número exterior', max_length=10)
    numero_int_poda = models.CharField('Número interior', max_length=10, blank=True, null=True)

    motivo_poda     = models.CharField(max_length=20, choices=MotivoPoda.choices)
    ubicacion_poda  = models.CharField(max_length=20, choices=UbicacionArbol.choices)
    foto_poda       = models.TextField(verbose_name='Imagen del árbol en Base64')
    referencias_poda = models.TextField('Referencias adicionales', blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estatus        = models.CharField(max_length=20, choices=Estatus.choices, default=Estatus.PENDIENTE)
    class Meta:
        verbose_name = 'Solicitud de Poda'
        verbose_name_plural = 'Solicitudes de Poda'
        ordering = ['-fecha_creacion']
    def __str__(self):
        return f"Solicitud #{self.pk} por {self.usuario.username} – {self.calle_poda}, {self.colonia_poda}"