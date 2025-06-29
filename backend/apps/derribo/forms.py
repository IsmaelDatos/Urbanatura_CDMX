from django import forms
from django.core.validators import FileExtensionValidator
from .models import SolicitudDerribo

class SolicitudDerriboForm(forms.ModelForm):
    latitud = forms.DecimalField(max_digits=9, decimal_places=6, required=True, widget=forms.HiddenInput())
    longitud = forms.DecimalField(max_digits=9, decimal_places=6, required=True, widget=forms.HiddenInput())
    foto_derribo = forms.ImageField(
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        widget=forms.FileInput(attrs={"accept": "image/*"})
    )
    justificacion_derribo = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="Describa en detalle por qué es necesario el derribo"
    )

    class Meta:
        model = SolicitudDerribo
        fields = [
            "latitud", "longitud",
            "motivo_derribo", "foto_derribo", "ubicacion_derribo",
            "calle_derribo", "numero_ext_derribo", "numero_int_derribo",
            "alcaldia_derribo", "colonia_derribo", "cp_derribo",
            "justificacion_derribo"
        ]
        widgets = {
            "motivo_derribo": forms.Select(attrs={"class": "form-control"}),
            "ubicacion_derribo": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)

    def clean_cp_derribo(self):
        cp = self.cleaned_data["cp_derribo"]
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