from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Usuario



class CiudadanoRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    latitud = forms.DecimalField(required=False, widget=forms.HiddenInput())
    longitud = forms.DecimalField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = Usuario
        fields = [
            'email', 'first_name', 'primer_apellido', 'segundo_apellido',
            'calle', 'num_ext', 'num_int', 'entidad_federativa',
            'municipio', 'codigo_postal', 'referencias',
            'latitud', 'longitud',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})
        self.fields['first_name'].required = True
        self.fields['primer_apellido'].required = True
        self.fields['codigo_postal'].validators = [
            RegexValidator(
                regex=r'^\d{5}$',
                message='El código postal debe tener 5 dígitos'
            )
        ]
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(username=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado")
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = 'CIUDADANO'
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class InstitucionRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    rfc = forms.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex='^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$',
                message='El RFC no tiene un formato válido'
            )
        ]
    )
    latitud = forms.DecimalField(required=False, widget=forms.HiddenInput())
    longitud = forms.DecimalField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = Usuario
        fields = [
            'nombre_institucion', 'rfc', 'email',
            'calle', 'num_ext', 'num_int', 'entidad_federativa',
            'municipio', 'codigo_postal', 'referencias',
            'latitud', 'longitud'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})
        self.fields['codigo_postal'].validators = [
            RegexValidator(
                regex='^[0-9]{5}$',
                message='El código postal debe tener 5 dígitos'
            )
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = 'INSTITUCION'
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nombre_institucion']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class CiudadanoEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'primer_apellido', 'segundo_apellido', 'telefono',
                 'calle', 'num_ext', 'num_int', 'municipio', 'codigo_postal', 'referencias']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo_postal'].validators = [
            RegexValidator(
                regex='^[0-9]{5}$',
                message='El código postal debe tener 5 dígitos'
            )
        ]

class InstitucionEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre_institucion', 'rfc', 'telefono',
            'calle', 'num_ext', 'num_int', 'municipio',
            'codigo_postal', 'referencias'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_institucion'].required = True
        self.fields['rfc'].required = True
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['rfc'].validators = [
            RegexValidator(
                regex=r'^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$',
                message='El RFC no tiene un formato válido'
            )
        ]
        self.fields['codigo_postal'].validators = [
            RegexValidator(
                regex=r'^[0-9]{5}$',
                message='El código postal debe tener 5 dígitos'
            )
        ]