from django.shortcuts import render,redirect,get_object_or_404
from .forms import ArbolForm
from .models import Arbol

def inicio(request):
    return render(request, 'arboles/inicio.html')

def agregar_arbol(request):
    if request.method == 'POST':
        form = ArbolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a la página de inicio después de guardar
    else:
        form = ArbolForm()
    return render(request, 'arboles/agregar_arbol.html', {'form': form})

def lista_arboles(request):
    arboles = Arbol.objects.all()  # Obtén todos los árboles de la base de datos
    return render(request, 'arboles/lista_arboles.html', {'arboles': arboles})

def modificar_arbol(request, id):
    arbol = get_object_or_404(Arbol, id=id)
    if request.method == 'POST':
        form = ArbolForm(request.POST, request.FILES, instance=arbol)
        if form.is_valid():
            form.save()
            return redirect('lista_arboles')
    else:
        form = ArbolForm(instance=arbol)
    return render(request, 'arboles/agregar_arbol.html', {'form': form})

def eliminar_arbol(request, id):
    arbol = get_object_or_404(Arbol, id=id)
    if request.method == 'POST':
        arbol.delete()
        return redirect('lista_arboles')
    return render(request, 'arboles/eliminar_arbol.html', {'arbol': arbol})

def documentacion(request):
    return render(request, 'arboles/documentacion.html')

def informacion_empresa(request):
    return render(request, 'arboles/informacion_empresa.html')