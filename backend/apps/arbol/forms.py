from django.core.exceptions import ValidationError
from django import forms
from .models import Arbol
class ArbolForm(forms.ModelForm):
    def validate_image_size(value):
        if value and value.size > 5 * 1024 * 1024:
            raise forms.ValidationError("El tamaño máximo de la imagen es 5 MB")
    foto1 = forms.ImageField(
        validators=[validate_image_size],
        required=True,
    )
    alcaldia = forms.CharField(max_length=100, required=True)
    estructura_general = forms.MultipleChoiceField(
        choices=Arbol.ESTRUCTURAS,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    inclinacion_terreno = forms.ChoiceField(
        choices=[
            ("plano", "Terreno plano"),
            ("ligera", "Inclinación ligera"),
            ("moderada", "Inclinación moderada"),
            ("pronunciada", "Inclinación pronunciada"),
        ],
        required=True,
    )

    class Meta:
        model = Arbol
        exclude = ["fecha_registro", "municipio_alcaldia"]
        widgets = {
            "fecha_registro": forms.HiddenInput(),
            "entidad_federativa": forms.TextInput(attrs={"readonly": True}),
            "nombre_cientifico": forms.TextInput(
                attrs={
                    "readonly": True,
                    "id": "nombre_cientifico_input",
                    "class": "p-2 rounded-lg border border-gray-300 bg-gray-100",
                }
            ),
            "codigo_postal": forms.TextInput(),
            "altura": forms.NumberInput(attrs={"step": "0.01"}),
            "diametro_tronco": forms.NumberInput(attrs={"step": "0.01"}),
            "diametro_copa": forms.NumberInput(attrs={"step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        defaults = {
            "entidad_federativa": "CDMX",
            "nombre_cientifico": "",
        }
        for field, value in defaults.items():
            if field in self.fields and not self.initial.get(field):
                self.fields[field].initial = value

    def clean_estructura_general(self):
        return self.cleaned_data.get("estructura_general", [])

    def clean_codigo_postal(self):
        cp = self.cleaned_data["codigo_postal"]
        if len(cp) != 5 or not cp.isdigit():
            raise forms.ValidationError("El código postal debe tener 5 dígitos")
        return cp

    def clean_altura(self):
        altura = self.cleaned_data["altura"]
        if altura <= 0 or altura > 50:
            raise forms.ValidationError("La altura debe estar entre 0 y 50 metros")
        return altura
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.municipio_alcaldia = self.cleaned_data.get("alcaldia")
        instance.estructura_general = self.cleaned_data.get(
            "estructura_general", []
        )
        if commit:
            instance.save()
            self.save_m2m()
        return instance