from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .forms import ArbolForm
from .models import Arbol
from django.http import JsonResponse
from .forms import ArbolForm
from django.conf import settings
import os

def inicio(request):
    return render(request, 'arboles/inicio.html')

def agregar_arbol(request):
    if request.method == 'POST':
        try:
            # Forzar valores del frontend
            post_data = request.POST.copy()
            post_data['entidad_federativa'] = 'CDMX'
            
            form = ArbolForm(post_data, request.FILES)
            
            if form.is_valid():
                arbol = form.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('arbol:lista_arboles')
                    })
                
                return redirect('arbol:lista_arboles')
                
            else:
                print("Errores de formulario:", form.errors)
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
                
        except Exception as e:
            print("Error en la vista:", str(e))
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    # GET request
    form = ArbolForm(initial={
        'entidad_federativa': 'CDMX',
    })
    return render(request, 'arboles/agregar_arbol.html', {'form': form})

def lista_arboles(request):
    try:
        arboles = Arbol.objects.all().order_by('-fecha_registro')
        return render(request, 'arboles/lista_arboles.html', {'arboles': arboles})
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'arboles/lista_arboles.html', {'arboles': []})

def modificar_arbol(request, id):
    arbol = get_object_or_404(Arbol, id=id)
    if request.method == 'POST':
        form = ArbolForm(request.POST, request.FILES, instance=arbol)
        if form.is_valid():
            form.save()
            return redirect('arbol:lista_arboles')
    else:
        form = ArbolForm(instance=arbol)
    return render(request, 'arboles/agregar_arbol.html', {'form': form})

def eliminar_arbol(request, id):
    arbol = get_object_or_404(Arbol, id=id)
    if request.method == 'POST':
        arbol.delete()
        return redirect('arbol:lista_arboles')  # Añadido namespace
    return render(request, 'arboles/eliminar_arbol.html', {'arbol': arbol})

def documentacion(request):
    return render(request, 'arboles/documentacion.html')

def informacion_empresa(request):
    return render(request, 'arboles/informacion_empresa.html')
    if request.method == 'POST':
        # Procesar formulario aquí
        return redirect('nombre_de_la_url_exitosa')
    return render(request, 'arboles/tu_template.html')
    # Tu lógica para guardar la solicitud aquí
    return render(request, 'arboles/solicitud_exitosa.html')