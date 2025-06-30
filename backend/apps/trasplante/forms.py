from django import forms
from django.core.validators import FileExtensionValidator
from .models import SolicitudTraslado
import base64

class SolicitudTrasladoForm(forms.ModelForm):
    latitud = forms.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'})
    )
    longitud = forms.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'})
    )
    foto_traslado_upload = forms.FileField(
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        widget=forms.FileInput(attrs={"accept": "image/*"}),
        label="Fotografía del árbol"
    )

    class Meta:
        model = SolicitudTraslado
        fields = [
            "latitud", "longitud",
            "motivo_traslado", "ubicacion_actual_traslado",
            "calle_actual_traslado", "numero_ext_actual_traslado", "numero_int_actual_traslado",
            "alcaldia_actual_traslado", "colonia_actual_traslado", "cp_actual_traslado",
            "calle_nueva_traslado", "numero_ext_nueva_traslado",
            "alcaldia_nueva_traslado", "colonia_nueva_traslado",
            "info_adicional_traslado"
        ]
        widgets = {
            "motivo_traslado": forms.Select(attrs={"class": "form-control"}),
            "ubicacion_actual_traslado": forms.Select(attrs={"class": "form-control"}),
            "info_adicional_traslado": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)
        # Establecer valores iniciales para coordenadas
        self.fields['latitud'].initial = '19.4326'
        self.fields['longitud'].initial = '-99.1332'
        
        # Hacer campos de nueva ubicación no requeridos inicialmente
        for field in ['calle_nueva_traslado', 'numero_ext_nueva_traslado', 
                     'alcaldia_nueva_traslado', 'colonia_nueva_traslado']:
            self.fields[field].required = False

    def clean_cp_actual_traslado(self):
        cp = self.cleaned_data["cp_actual_traslado"]
        if len(cp) != 5 or not cp.isdigit():
            raise forms.ValidationError("El código postal debe tener 5 dígitos")
        return cp

    def clean_foto_traslado_upload(self):
        uploaded_file = self.cleaned_data.get('foto_traslado_upload')
        if not uploaded_file:
            raise forms.ValidationError("Debe subir una fotografía del árbol")
        
        if uploaded_file.size > 5 * 1024 * 1024:  # 5MB
            raise forms.ValidationError("La imagen no debe exceder los 5MB")
        
        content_type = uploaded_file.content_type
        if content_type not in ['image/jpeg', 'image/png']:
            raise forms.ValidationError("Solo se permiten imágenes JPEG o PNG")
        
        try:
            encoded_string = base64.b64encode(uploaded_file.read()).decode('utf-8')
            return f"data:{content_type};base64,{encoded_string}"
        except Exception as e:
            raise forms.ValidationError(f"Error procesando la imagen: {str(e)}")

    def clean(self):
        cleaned_data = super().clean()
        motivo = cleaned_data.get("motivo_traslado")
        
        # Validar campos de nueva ubicación si el motivo es "mejor_ubicacion"
        if motivo == "mejor_ubicacion":
            campos_requeridos = {
                'calle_nueva_traslado': 'Debe especificar la calle de la nueva ubicación',
                'alcaldia_nueva_traslado': 'Debe especificar la alcaldía de la nueva ubicación',
                'colonia_nueva_traslado': 'Debe especificar la colonia de la nueva ubicación'
            }
            
            for campo, mensaje in campos_requeridos.items():
                if not cleaned_data.get(campo):
                    self.add_error(campo, mensaje)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.usuario:
            instance.usuario = self.usuario
        
        # Asignar la imagen en Base64 al campo del modelo
        instance.foto_traslado = self.cleaned_data.get('foto_traslado_upload', '')
        
        if commit:
            instance.save()
        return instance