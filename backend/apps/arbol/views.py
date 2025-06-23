from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.conf import settings
from .forms import CiudadanoRegistrationForm, InstitucionRegistrationForm, LoginForm
import os

def register_ciudadano(request):
    if request.method == 'GET':
        template_path = os.path.join(settings.BASE_DIR, 'backend', 'urbanatura_cdmx', 'templates', 'registration', 'register.html')
        if not os.path.exists(template_path):
            return JsonResponse({
                'success': False,
                'error': 'Template no encontrado'
            }, status=500)

        return render(request, 'registration/register.html', {
            'form': CiudadanoRegistrationForm(),
            'STATIC_URL': settings.STATIC_URL
        })
    
    elif request.method == 'POST':
        try:
            form = CiudadanoRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/'
                })
            
            # Mejor manejo de errores del formulario
            errors = {}
            for field, error_list in form.errors.items():
                if field == '__all__':
                    errors['non_field_errors'] = error_list
                else:
                    errors[field] = error_list[0] if error_list else 'Error desconocido'
            
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
            
        except Exception as e:
            # Log del error para diagnóstico
            print(f"Error en register_ciudadano: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Error interno del servidor'
            }, status=500)
    
    return HttpResponseNotAllowed(['GET', 'POST'])

def register_institucion(request):
    if request.method == 'GET':
        # Verificar si el template existe
        template_path = os.path.join(settings.BASE_DIR, 'backend', 'urbanatura_cdmx', 'templates', 'registration', 'register_institucion.html')
        if not os.path.exists(template_path):
            return JsonResponse({
                'success': False,
                'error': 'Template no encontrado'
            }, status=500)

        return render(request, 'registration/register_institucion.html', {
            'form': InstitucionRegistrationForm(),
            'STATIC_URL': settings.STATIC_URL
        })
    
    elif request.method == 'POST':
        try:
            form = InstitucionRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Registro exitoso como institución',
                    'redirect_url': '/'
                })
            
            # Manejo mejorado de errores
            errors = {}
            for field, error_list in form.errors.items():
                if field == '__all__':
                    errors['non_field_errors'] = error_list
                else:
                    errors[field] = error_list[0] if error_list else 'Error desconocido'
            
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
            
        except Exception as e:
            print(f"Error en register_institucion: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Error interno del servidor'
            }, status=500)
    
    return JsonResponse({
        'success': False, 
        'error': 'Método no permitido'
    }, status=405)

def user_login(request):
    if request.method == 'GET':
        # Verificar template
        template_path = os.path.join(settings.BASE_DIR, 'backend', 'urbanatura_cdmx', 'templates', 'registration', 'login.html')
        if not os.path.exists(template_path):
            return JsonResponse({
                'success': False,
                'error': 'Template no encontrado'
            }, status=500)

        return render(request, 'registration/login.html', {
            'form': LoginForm(),
            'STATIC_URL': settings.STATIC_URL
        })
    
    elif request.method == 'POST':
        try:
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
                        'error': 'Correo electrónico o contraseña incorrectos'
                    }, status=400)
            
            # Manejo de errores del formulario
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0] if error_list else 'Error desconocido'
            
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
            
        except Exception as e:
            print(f"Error en user_login: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Error interno del servidor'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    }, status=405)

def user_logout(request):
    try:
        logout(request)
        return redirect('arbol:inicio')
    except Exception as e:
        print(f"Error en user_logout: {str(e)}")
        return redirect('arbol:inicio')