from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class Usuario(AbstractUser):
    """Modelo de usuario extendido para ciudadanos e instituciones."""
    TIPO_USUARIO = [
        ('CIUDADANO', 'Ciudadano'),
        ('INSTITUCION', 'Institución'),
    ]
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=11, choices=TIPO_USUARIO)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    calle = models.CharField(max_length=100)
    num_ext = models.CharField(max_length=10)
    num_int = models.CharField(max_length=10, blank=True, null=True)
    entidad_federativa = models.CharField(max_length=50, default='CDMX')
    municipio = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=5)
    referencias = models.TextField(blank=True, null=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    primer_apellido = models.CharField(max_length=50, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    nombre_institucion = models.CharField(max_length=100, blank=True, null=True)
    rfc = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$',
                message='El RFC no tiene un formato válido',
            )
        ],
    )
    def __str__(self):
        if self.tipo_usuario == 'CIUDADANO':
            nombre = f"{self.first_name} {self.primer_apellido}".strip()
            return f"{nombre or self.email} (Ciudadano)"
        return f"{self.nombre_institucion or self.email} (Institución)"

    def save(self, *args, **kwargs):
        """
        • Establece el email como username si no se proporcionó otro.
        • Normaliza el email a minúsculas antes de guardar.
        """
        if not self.username:
            self.username = self.email
        self.email = self.email.lower()
        super().save(*args, **kwargs)
