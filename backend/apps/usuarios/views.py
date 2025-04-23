from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CiudadanoRegistrationForm, InstitucionRegistrationForm, LoginForm
from django.http import HttpResponseNotAllowed

def register_ciudadano(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html', {
            'form': CiudadanoRegistrationForm()
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
            
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0] if error_list else 'Error desconocido'
            
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return HttpResponseNotAllowed(['GET', 'POST'])

def register_institucion(request):
    if request.method == 'GET':
        return render(request, 'registration/register_institucion.html', {
            'form': InstitucionRegistrationForm()
        })
    
    elif request.method == 'POST':
        form = InstitucionRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Registro exitoso como institución',
                'redirect_url': '/'
            })
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({
                'success': False,
                'error': 'Datos inválidos',
                'errors': errors
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

def user_login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {
            'form': LoginForm()
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