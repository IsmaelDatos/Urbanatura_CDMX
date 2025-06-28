from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import CiudadanoRegistrationForm, InstitucionRegistrationForm, LoginForm, CiudadanoEditForm, InstitucionEditForm
from django.conf import settings
from django.db import IntegrityError

def _register(request, form_class, template_name, tipo_usuario):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.latitud = form.cleaned_data.get("latitud")
                user.longitud = form.cleaned_data.get("longitud")
                user.tipo_usuario = tipo_usuario
                user.save()
                login(request, user)
                redirect_url = (
                    reverse("home_ciudadano")
                    if tipo_usuario == "CIUDADANO"
                    else reverse("home_institucion")
                )
                return redirect(redirect_url)
            except IntegrityError:
                form.add_error("email", "Este correo electrónico ya está registrado")
        return render(
            request,
            template_name,
            {
                "form": form,
                "preserve_data": True,
            },
        )
    return render(request, template_name, {"form": form_class()})

@require_http_methods(["GET", "POST"])
def register_ciudadano(request):
    """Registro de ciudadanos."""
    return _register(
        request,
        form_class=CiudadanoRegistrationForm,
        template_name="registration/register.html",
        tipo_usuario="CIUDADANO",
    )

@require_http_methods(["GET", "POST"])
def register_institucion(request):
    """Registro de instituciones."""
    return _register(
        request,
        form_class=InstitucionRegistrationForm,
        template_name="registration/register.html",
        tipo_usuario="INSTITUCION",
    )

def user_login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {
                'form': LoginForm(),
                'STATIC_URL': settings.STATIC_URL
            })
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Credenciales inválidas'
                }, status=400)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Formulario inválido'
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

def user_logout(request):
    logout(request)
    return redirect('arbol:inicio')

@login_required
def home_ciudadano(request):
    return render(request, 'home/home_ciudadano.html')

@login_required
def home_institucion(request):
    return render(request, 'home/home_institucion.html', {
        'institucion': request.user
    })

@login_required
def edit_ciudadano(request):
    if request.method == 'POST':
        form = CiudadanoEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('home_ciudadano')
                })
            return redirect('home_ciudadano')
    else:
        form = CiudadanoEditForm(instance=request.user)
    
    return render(request, 'usuarios/edit_ciudadano.html', {'form': form})

@login_required
def edit_institucion(request):
    if request.method == 'POST':
        form = InstitucionEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil institucional actualizado correctamente')
            return redirect('home_institucion')
    else:
        form = InstitucionEditForm(instance=request.user)
    
    return render(request, 'usuarios/edit_institucion.html', {
        'form': form,
        'STATIC_URL': settings.STATIC_URL
    })