from django import forms
from .models import SolicitudPoda
from django.core.validators import FileExtensionValidator

class SolicitudPodaForm(forms.ModelForm):
    foto_poda = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
    
    class Meta:
        model = SolicitudPoda
        fields = [
            'motivo_poda', 
            'foto_poda', 
            'ubicacion_poda',
            'calle_poda',
            'numero_ext_poda',
            'numero_int_poda',
            'alcaldia_poda',
            'colonia_poda',
            'cp_poda',
            'referencias_poda'
        ]
        widgets = {
            'motivo_poda': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion_poda': forms.Select(attrs={'class': 'form-control'}),
            'referencias_poda': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.usuario:
            instance.usuario = self.usuario
        if commit:
            instance.save()
        return instance