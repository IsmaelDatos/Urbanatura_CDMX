from django import forms
from django.core.validators import FileExtensionValidator
from .models import SolicitudTraslado


class SolicitudTrasladoForm(forms.ModelForm):
    latitud = forms.DecimalField(max_digits=9, decimal_places=6, required=True, widget=forms.HiddenInput())
    longitud = forms.DecimalField(max_digits=9, decimal_places=6, required=True, widget=forms.HiddenInput())
    foto_traslado = forms.ImageField(
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        widget=forms.FileInput(attrs={"accept": "image/*"})
    )
    info_adicional_traslado = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="Describa las características del árbol y razones para el traslado"
    )

    class Meta:
        model = SolicitudTraslado
        fields = [
            "latitud", "longitud",
            "motivo_traslado", "foto_traslado",
            "ubicacion_actual_traslado", "calle_actual_traslado",
            "numero_ext_actual_traslado", "numero_int_actual_traslado",
            "alcaldia_actual_traslado", "colonia_actual_traslado",
            "cp_actual_traslado", "calle_nueva_traslado",
            "numero_ext_nueva_traslado", "alcaldia_nueva_traslado",
            "colonia_nueva_traslado", "info_adicional_traslado"
        ]
        widgets = {
            "motivo_traslado": forms.Select(attrs={"class": "form-control"}),
            "ubicacion_actual_traslado": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "calle_nueva_traslado": "Calle (nueva ubicación)",
            "numero_ext_nueva_traslado": "Número exterior (nueva ubicación)",
            "alcaldia_nueva_traslado": "Alcaldía (nueva ubicación)",
            "colonia_nueva_traslado": "Colonia (nueva ubicación)",
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)
        for field in [
            "calle_nueva_traslado",
            "numero_ext_nueva_traslado",
            "alcaldia_nueva_traslado",
            "colonia_nueva_traslado"
        ]:
            self.fields[field].required = False

    def clean_cp_actual_traslado(self):
        cp = self.cleaned_data["cp_actual_traslado"]
        if len(cp) != 5 or not cp.isdigit():
            raise forms.ValidationError("El código postal debe tener 5 dígitos")
        return cp

    def clean(self):
        cleaned_data = super().clean()
        motivo = cleaned_data.get("motivo_traslado")
        if motivo == "mejor_ubicacion":
            for campo in [
                "calle_nueva_traslado",
                "alcaldia_nueva_traslado",
                "colonia_nueva_traslado"
            ]:
                if not cleaned_data.get(campo):
                    self.add_error(campo, "Este campo es requerido para este motivo de traslado")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.usuario:
            instance.usuario = self.usuario
        if commit:
            instance.save()
            self.save_m2m()
        return instance