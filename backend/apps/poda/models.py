from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class SolicitudPoda(models.Model):
    class MotivoPoda(models.TextChoices):
        MANTENIMIENTO = 'mantenimiento', _('Mantenimiento preventivo')
        SEGURIDAD = 'seguridad', _('Seguridad (ramas peligrosas)')
        SALUD = 'salud', _('Salud del árbol')
        INTERFERENCIA = 'interferencia', _('Interferencia con infraestructura')

    class Ubicacion(models.TextChoices):
        BANQUETA = 'banqueta', _('Banqueta')
        CAMELLON = 'camellon', _('Camellón')
        GLORIETA = 'glorieta', _('Glorieta')
        PARQUE = 'parque', _('Parque')

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_poda')
    motivo_poda = models.CharField(max_length=20, choices=MotivoPoda.choices)
    foto_poda = models.ImageField(upload_to='poda/')
    ubicacion_poda = models.CharField(max_length=20, choices=Ubicacion.choices)
    calle_poda = models.CharField(max_length=100)
    numero_ext_poda = models.CharField(max_length=10)
    numero_int_poda = models.CharField(max_length=10, blank=True, null=True)
    alcaldia_poda = models.CharField(max_length=50)
    colonia_poda = models.CharField(max_length=50)
    cp_poda = models.CharField(max_length=5)
    referencias_poda = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=20, default='pendiente', 
                              choices=[('pendiente', 'Pendiente'), 
                                      ('aprobada', 'Aprobada'), 
                                      ('rechazada', 'Rechazada')])

    class Meta:
        verbose_name = 'Solicitud de Poda'
        verbose_name_plural = 'Solicitudes de Poda'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Solicitud de poda #{self.id} - {self.usuario.email}"