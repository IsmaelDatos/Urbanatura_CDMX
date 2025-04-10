from django.db import models
from django.utils import timezone

class Arbol(models.Model):
    # Opciones para choices
    ESTRUCTURAS = [
        ('copa mal equilibrada', 'Copa mal equilibrada'),
        ('ramas muy largas', 'Ramas muy largas'),
        ('troncos múltiples', 'Troncos múltiples'),
        ('troncos codominantes', 'Troncos codominantes'),
        ('ramas codominantes', 'Ramas codominantes'),
    ]
    
    CONDICIONES = [
        ('irrecuperable', 'Irrecuperable'),
        ('susceptible de mejora', 'Susceptible de mejora'),
        ('buena', 'Buena'),
        ('muy buena', 'Muy buena'),
    ]
    
    UBICACION_CHOICES = [
        ('Banqueta', 'Banqueta'),
        ('Camellón', 'Camellón'),
        ('Glorieta', 'Glorieta'),
        ('Parque', 'Parque'),
        ('Arriate', 'Arriate'),
        ('Plaza', 'Plaza'),
        ('Propiedad privada', 'Propiedad privada'),
        ('Obra civil', 'Obra civil'),
        ('Otro', 'Otro'),
    ]

    # Localización
    entidad_federativa = models.CharField(max_length=100, default="Ciudad de México")
    codigo_postal = models.CharField(max_length=5)
    municipio_alcaldia = models.CharField(max_length=100)
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=255)
    num_ext = models.CharField(max_length=10, blank=True, null=True)
    num_int = models.CharField(max_length=10, blank=True, null=True)
    entre_calle = models.CharField(max_length=100, blank=True, null=True)
    y_calle = models.CharField(max_length=100, blank=True, null=True)
    ubicacion = models.CharField(max_length=50, choices=UBICACION_CHOICES,blank=True,)
    ubicacion_otro = models.CharField(max_length=100, blank=True, null=True)
    
    # Características del árbol
    nombre_comun = models.CharField(max_length=100)
    nombre_cientifico = models.CharField(max_length=100)
    numero_arbol = models.CharField(max_length=50, blank=True, null=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    diametro_tronco = models.DecimalField(max_digits=5, decimal_places=2)
    diametro_copa = models.DecimalField(max_digits=5, decimal_places=2)
    inclinacion_tronco = models.CharField(max_length=50)
    estructura_general = models.CharField(max_length=50, choices=ESTRUCTURAS)
    condicion_general = models.CharField(max_length=50, choices=CONDICIONES)
    
    # Metadata y fotos
    fecha_registro = models.DateField(default=timezone.now)
    foto1 = models.ImageField(upload_to='arboles/')
    foto2 = models.ImageField(upload_to='arboles/', blank=True, null=True)
    foto3 = models.ImageField(upload_to='arboles/', blank=True, null=True)
    foto4 = models.ImageField(upload_to='arboles/', blank=True, null=True)
    foto5 = models.ImageField(upload_to='arboles/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_comun} - {self.calle}, {self.colonia}"