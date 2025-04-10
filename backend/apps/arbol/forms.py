from django.core.exceptions import ValidationError
from django import forms
from .models import Arbol

class ArbolForm(forms.ModelForm):
    def validate_image_size(value):
        if value:
            filesize = value.size
            if filesize > 5 * 1024 * 1024:  # 5MB
                raise ValidationError("El tamaño máximo de la imagen es 5MB")

    foto1 = forms.ImageField(validators=[validate_image_size], required=True)
    alcaldia = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Arbol
        exclude = ['fecha_registro', 'municipio_alcaldia']
        widgets = {
            'fecha_registro': forms.HiddenInput(),
            'entidad_federativa': forms.TextInput(attrs={'readonly': True}),
            'nombre_cientifico': forms.TextInput(attrs={
                'readonly': True,
                'id': 'nombre_cientifico_input',
                'class': 'p-2 rounded-lg border border-gray-300 bg-gray-100'
            }),
            'codigo_postal': forms.TextInput(),
            'altura': forms.NumberInput(attrs={'step': '0.01'}),
            'diametro_tronco': forms.NumberInput(attrs={'step': '0.01'}),
            'diametro_copa': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Elimina esta línea que causa el error
        # self.fields['foto'].required = False
        
        self.fields['entidad_federativa'].initial = "CDMX"
        self.fields['nombre_cientifico'].initial = ""
        self.fields['nombre_cientifico'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.municipio_alcaldia = self.cleaned_data['alcaldia']
        
        if commit:
            instance.save()
            self.save_m2m()  # Importante para guardar relaciones ManyToMany si las hay
        return instance
    