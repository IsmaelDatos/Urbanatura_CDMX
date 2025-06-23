from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .forms import ArbolForm
from .models import Arbol
from django.http import JsonResponse
from .forms import ArbolForm
from django.conf import settings
import os
# import geopandas as gpd
import folium

def inicio(request):
    m = folium.Map(
        location=[19.4326, -99.1332], 
        tiles="cartodbpositron",
        zoom_start=12
    )
    map_html = m._repr_html_()
    context = {
        'map_html': map_html
    }
    return render(request, 'arboles/inicio.html', context)

def agregar_arbol(request):
    if request.method == 'POST':
        try:
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
        return redirect('arbol:lista_arboles') 
    return render(request, 'arboles/eliminar_arbol.html', {'arbol': arbol})

def documentacion(request):
    return render(request, 'arboles/documentacion.html')

def informacion_empresa(request):
    return render(request, 'arboles/informacion_empresa.html')