from django import forms
from .models import Arbol  

class ArbolForm(forms.ModelForm):
    class Meta:
        model = Arbol
        fields = ['foto', 'calle', 'codigo_postal', 'delegacion', 'ciudad', 'estado', 'tiene_plaga']  # Especifica los campos que deseas incluir