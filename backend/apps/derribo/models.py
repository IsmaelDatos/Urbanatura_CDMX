from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

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

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_derribo')
    motivo_derribo = models.CharField(max_length=20, choices=MotivoDerribo.choices)
    foto_derribo = models.ImageField(upload_to='derribo/')
    ubicacion_derribo = models.CharField(max_length=20, choices=Ubicacion.choices)
    calle_derribo = models.CharField(max_length=100)
    numero_ext_derribo = models.CharField(max_length=10)
    numero_int_derribo = models.CharField(max_length=10, blank=True, null=True)
    alcaldia_derribo = models.CharField(max_length=50)
    colonia_derribo = models.CharField(max_length=50)
    cp_derribo = models.CharField(max_length=5)
    justificacion_derribo = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=20, default='pendiente', 
                              choices=[('pendiente', 'Pendiente'), 
                                      ('aprobada', 'Aprobada'), 
                                      ('rechazada', 'Rechazada'),
                                      ('requiere_aprobacion', 'Requiere aprobación especial')])

    class Meta:
        verbose_name = 'Solicitud de Derribo'
        verbose_name_plural = 'Solicitudes de Derribo'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Solicitud de derribo #{self.id} - {self.usuario.email}"