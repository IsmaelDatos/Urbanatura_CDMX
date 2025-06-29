from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import SolicitudTraslado
from .forms import SolicitudTrasladoForm
from django.http import JsonResponse
from django.shortcuts import redirect


class CrearSolicitudTrasladoView(LoginRequiredMixin, CreateView):
    model = SolicitudTraslado
    form_class = SolicitudTrasladoForm
    template_name = "tramites/trasplante.html"
    success_url = reverse_lazy("traslado:lista")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario"] = self.request.user
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)  # El usuario ya se asigna en el form.save()
        instance.latitud = form.cleaned_data["latitud"]
        instance.longitud = form.cleaned_data["longitud"]
        try:
            instance.save()
            if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True,
                    "message": "Solicitud de trasplante creada exitosamente. Requerirá inspección técnica."
                })
            messages.success(
                self.request, 
                "Solicitud de trasplante creada exitosamente. Requerirá inspección técnica."
            )
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Error al guardar solicitud: {str(e)}")
            return self.form_invalid(form)

class ListaSolicitudesTrasladoView(LoginRequiredMixin, ListView):
    model = SolicitudTraslado
    template_name = 'traslado/lista_solicitudes.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        return SolicitudTraslado.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')

class DetalleSolicitudTrasladoView(LoginRequiredMixin, DetailView):
    model = SolicitudTraslado
    template_name = 'traslado/detalle_solicitud.html'
    context_object_name = 'solicitud'

    def get_queryset(self):
        return SolicitudTraslado.objects.filter(usuario=self.request.user)