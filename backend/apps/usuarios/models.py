from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('CIUDADANO', 'Ciudadano'),
        ('INSTITUCION', 'Institución'),
    ]
    
    tipo_usuario = models.CharField(max_length=11, choices=TIPO_USUARIO)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    # Campos comunes para dirección
    calle = models.CharField(max_length=100)
    num_ext = models.CharField(max_length=10)
    num_int = models.CharField(max_length=10, blank=True, null=True)
    entidad_federativa = models.CharField(max_length=50, default='CDMX')
    municipio = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=5)
    referencias = models.TextField(blank=True, null=True)
    
    # Campos específicos para ciudadano
    primer_apellido = models.CharField(max_length=50, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    
    # Campos específicos para institución
    nombre_institucion = models.CharField(max_length=100, blank=True, null=True)
    rfc = models.CharField(
        max_length=13, 
        blank=True, 
        null=True,
        validators=[
            RegexValidator(
                regex='^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$',
                message='El RFC no tiene un formato válido'
            )
        ]
    )

    def __str__(self):
        if self.tipo_usuario == 'CIUDADANO':
            return f"{self.first_name} {self.primer_apellido} (Ciudadano)"
        return f"{self.nombre_institucion} (Institución)"