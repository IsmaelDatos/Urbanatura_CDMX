from django import forms
from .models import SolicitudPoda

class SolicitudPodaForm(forms.ModelForm):
    class Meta:
        model = SolicitudPoda
        fields = [
            'motivo_poda', 'foto', 'ubicacion', 'calle', 'num_ext', 'num_int', 
            'entidad_federativa', 'municipio', 'codigo_postal', 'referencias'
        ]
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'motivo_poda': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'ubicacion': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'calle': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'num_ext': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'num_int': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'entidad_federativa': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'municipio': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'referencias': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        }
