from django import forms
from django.core.validators import FileExtensionValidator
from .models import SolicitudPoda


class SolicitudPodaForm(forms.ModelForm):
    latitud = forms.DecimalField(max_digits=9, decimal_places=6, required=True, widget=forms.HiddenInput())
    longitud = forms.DecimalField(max_digits=9, decimal_places=6, required=True, widget=forms.HiddenInput())
    foto_poda = forms.ImageField(
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        widget=forms.FileInput(attrs={"accept": "image/*"})
    )
    referencias_poda = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = SolicitudPoda
        fields = [
            "latitud", "longitud",
            "motivo_poda", "foto_poda", "ubicacion_poda",
            "calle_poda", "numero_ext_poda", "numero_int_poda",
            "alcaldia_poda", "colonia_poda", "cp_poda",
            "referencias_poda"
        ]
        widgets = {
            "motivo_poda": forms.Select(attrs={"class": "form-control"}),
            "ubicacion_poda": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)

    def clean_cp_poda(self):
        cp = self.cleaned_data["cp_poda"]
        if len(cp) != 5 or not cp.isdigit():
            raise forms.ValidationError("El código postal debe tener 5 dígitos")
        return cp

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.usuario:
            instance.usuario = self.usuario
        if commit:
            instance.save()
            self.save_m2m()
        return instance