from django.db import models

class Arbol(models.Model):
    foto = models.ImageField(upload_to='arboles/')
    calle = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=5)
    delegacion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100, default="Ciudad de México")
    estado = models.CharField(max_length=100, default="Ciudad de México")
    fecha_registro = models.DateField(auto_now_add=True)
    tiene_plaga = models.BooleanField(default=False)

    def __str__(self):
        return f"Árbol en {self.calle}, {self.delegacion}"