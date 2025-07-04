from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .forms import ArbolForm
from .models import Arbol
from django.http import JsonResponse
import base64
from django.conf import settings
from django.db import transaction, IntegrityError
import logging
from apps.poda.models import SolicitudPoda
from django.contrib.auth.decorators import login_required
from apps.derribo.models import SolicitudDerribo
from apps.trasplante.models import SolicitudTraslado
from apps.usuarios.models import Usuario

logger = logging.getLogger(__name__)

def inicio(request):
    return render(request, 'arboles/inicio.html')

def agregar_arbol(request):
    logger.debug(f"Request method: {request.method}")
    if request.method == "POST":
        logger.debug("POST request received")
        form = ArbolForm(request.POST, request.FILES, request=request)
        try:
            with transaction.atomic():
                if not form.is_valid():
                    errors = {
                        field: [str(e) for e in error_list]
                        for field, error_list in form.errors.items()
                    }
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        if not form.is_valid():
                            return JsonResponse({"success": False, "errors": form.errors.get_json_data()}, status=400)
                        return JsonResponse({
                            "success": True,
                            "message": "Árbol registrado exitosamente",
                            "redirect_url": reverse("arbol:lista_arboles")
                        }, status=200)
                lat = form.cleaned_data.get("latitud")
                lng = form.cleaned_data.get("longitud")
                existing = (
                    Arbol.objects.select_for_update()
                    .filter(latitud=lat, longitud=lng)
                    .first()
                )
                if existing:
                    error_msg = "Ya existe un árbol registrado en estas coordenadas"
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse(
                            {"success": False, "error": error_msg, "field": "coordenadas"},
                            status=400,
                        )
                    form.add_error(None, error_msg)
                    return render(request, "arboles/agregar_arbol.html", {"form": form})
                arbol = form.save(commit=False)
                if "foto1" in request.FILES:
                    arbol.foto1 = base64.b64encode(request.FILES["foto1"].read()).decode("utf-8")
                for i in range(2, 6):
                    foto_field = f"foto{i}"
                    if foto_field in request.FILES:
                        setattr(
                            arbol,
                            foto_field,
                            base64.b64encode(request.FILES[foto_field].read()).decode("utf-8"),
                        )
                try:
                    arbol.save()
                    form.save_m2m()
                except IntegrityError:
                    error_msg = "Ya existe un árbol registrado en estas coordenadas"
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse(
                            {"success": False, "error": error_msg, "field": "coordenadas"},
                            status=400,
                        )
                    form.add_error(None, error_msg)
                    return render(request, "arboles/agregar_arbol.html", {"form": form})
                response_data = {
                    "success": True,
                    "message": "Árbol registrado exitosamente",
                    "redirect_url": request.build_absolute_uri(reverse("arbol:lista_arboles")),
                    "arbol_id": arbol.id,
                }
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse(response_data)
                messages.success(request, response_data["message"])
                return redirect(response_data["redirect_url"])
        except Exception as e:
            error_msg = str(e) if settings.DEBUG else "Error interno del servidor"
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": error_msg}, status=500)
            messages.error(request, "Ocurrió un error al procesar tu solicitud")
            return redirect("arbol:agregar_arbol")
    form = ArbolForm(request=request)
    return render(request, "arboles/agregar_arbol.html", {"form": form})
    logger.debug(f"Redirecting to: {response_data['redirect_url']}")
    return JsonResponse(response_data)

def modificar_arbol(request, id):
    arbol = get_object_or_404(Arbol, id=id)
    if request.method == 'POST':
        form = ArbolForm(request.POST, request.FILES, instance=arbol)
        if form.is_valid():
            arbol_actualizado = form.save(commit=False)
            for i in range(1, 6):
                foto_field = f'foto{i}'
                if foto_field in request.FILES:
                    imagen = request.FILES[foto_field]
                    arbol_actualizado.__dict__[foto_field] = base64.b64encode(imagen.read()).decode('utf-8')
            
            arbol_actualizado.save()
            return redirect('arbol:lista_arboles')
    else:
        form = ArbolForm(instance=arbol)
    return render(request, 'arboles/agregar_arbol.html', {'form': form})

def lista_arboles(request):
    try:
        arboles = Arbol.objects.all().order_by('-fecha_registro')
        return render(request, 'arboles/lista_arboles.html', {'arboles': arboles})
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'arboles/lista_arboles.html', {'arboles': []})

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

def datos_mapa(request):
    arboles = Arbol.objects.all().values(
        'id', 'latitud', 'longitud', 'diametro_tronco', 'condicion_general'
    )
    
    podas = SolicitudPoda.objects.all().values(
        'id', 'latitud', 'longitud'
    )
    
    derribos = SolicitudDerribo.objects.all().values(
        'id', 'latitud', 'longitud'
    )
    
    return JsonResponse({
        'arboles': list(arboles),
        'podas': list(podas),
        'derribos': list(derribos)
    })
    
@login_required
def home_ciudadano(request):
    context = {
        "solicitudes_poda":     SolicitudPoda.objects.filter(usuario=request.user)
                               .order_by("-fecha_creacion")[:5],
        "solicitudes_derribo":  SolicitudDerribo.objects.filter(usuario=request.user)
                               .order_by("-fecha_creacion")[:5],
        "solicitudes_traslado": SolicitudTraslado.objects.filter(usuario=request.user)
                               .order_by("-fecha_creacion")[:5],
    }
    return render(request, "home/home_ciudadano.html", context)

@login_required
def home_institucion(request):
    if request.user.tipo_usuario != "INSTITUCION":
        return redirect("home_ciudadano")

    context = {
        "institucion": request.user,
        "solicitudes_poda":     SolicitudPoda.objects.filter(usuario=request.user)
                               .order_by("-fecha_creacion")[:10],
        "solicitudes_derribo":  SolicitudDerribo.objects.filter(usuario=request.user)
                               .order_by("-fecha_creacion")[:10],
        "solicitudes_traslado": SolicitudTraslado.objects.filter(usuario=request.user)
                               .order_by("-fecha_creacion")[:10],
    }
    return render(request, "home/home_institucion.html", context)