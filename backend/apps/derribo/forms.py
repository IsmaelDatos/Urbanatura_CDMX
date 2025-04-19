from django import forms
from .models import SolicitudDerribo
from django.core.validators import FileExtensionValidator

class SolicitudDerriboForm(forms.ModelForm):
    foto_derribo = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
    justificacion_derribo = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Describa en detalle por qué es necesario el derribo"
    )
    
    class Meta:
        model = SolicitudDerribo
        fields = [
            'motivo_derribo', 
            'foto_derribo', 
            'ubicacion_derribo',
            'calle_derribo',
            'numero_ext_derribo',
            'numero_int_derribo',
            'alcaldia_derribo',
            'colonia_derribo',
            'cp_derribo',
            'justificacion_derribo'
        ]
        widgets = {
            'motivo_derribo': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion_derribo': forms.Select(attrs={'class': 'form-control'}),
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