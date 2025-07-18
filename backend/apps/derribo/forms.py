from django import forms
from django.core.validators import FileExtensionValidator
from .models import SolicitudDerribo
import base64

class SolicitudDerriboForm(forms.ModelForm):
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
    foto_derribo_upload = forms.FileField(
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        widget=forms.FileInput(attrs={"accept": "image/*"}),
        label="Fotografía del árbol"
    )
    
    justificacion_derribo = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        label="Justificación del derribo"
    )

    class Meta:
        model = SolicitudDerribo
        fields = [
            "latitud", "longitud",
            "motivo_derribo", "ubicacion_derribo",
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
        # Establecer valores iniciales para coordenadas
        self.fields['latitud'].initial = '19.4326'
        self.fields['longitud'].initial = '-99.1332'

    def clean_cp_derribo(self):
        cp = self.cleaned_data["cp_derribo"]
        if len(cp) != 5 or not cp.isdigit():
            raise forms.ValidationError("El código postal debe tener 5 dígitos")
        return cp

    def clean_foto_derribo_upload(self):
        uploaded_file = self.cleaned_data.get('foto_derribo_upload')
        if not uploaded_file:
            raise forms.ValidationError("Debe subir una fotografía del árbol")
        
        if uploaded_file.size > 5 * 1024 * 1024:  # 5MB
            raise forms.ValidationError("La imagen no debe exceder los 5MB")
        
        # Validar tipo de contenido
        content_type = uploaded_file.content_type
        if content_type not in ['image/jpeg', 'image/png']:
            raise forms.ValidationError("Solo se permiten imágenes JPEG o PNG")
        
        try:
            # Leer y convertir a Base64
            encoded_string = base64.b64encode(uploaded_file.read()).decode('utf-8')
            return f"data:{content_type};base64,{encoded_string}"
        except Exception as e:
            raise forms.ValidationError(f"Error procesando la imagen: {str(e)}")

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Asignar usuario y procesar imagen
        if self.usuario:
            instance.usuario = self.usuario
        
        # Asignar la imagen en Base64 al campo del modelo
        instance.foto_derribo = self.cleaned_data.get('foto_derribo_upload', '')
        
        if commit:
            try:
                instance.save()
            except Exception as e:
                print(f"Error al guardar: {str(e)}")
                raise
        return instance