from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import SolicitudDerribo
from .forms import SolicitudDerriboForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect


class CrearSolicitudDerriboView(LoginRequiredMixin, CreateView):
    model = SolicitudDerribo
    form_class = SolicitudDerriboForm
    template_name = "tramites/derribo.html"
    success_url = reverse_lazy("derribo:lista")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario"] = self.request.user
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.latitud = form.cleaned_data["latitud"]
        instance.longitud = form.cleaned_data["longitud"]  
        try:
            instance.save()
            if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True, 
                    "message": "Solicitud de derribo creada exitosamente"
                })
            messages.success(self.request, "Solicitud de derribo creada exitosamente")
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Error al guardar solicitud: {str(e)}")
            return self.form_invalid(form)

class ListaSolicitudesDerriboView(LoginRequiredMixin, ListView):
    model = SolicitudDerribo
    template_name = 'derribo/lista_solicitudes.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        return SolicitudDerribo.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')

class DetalleSolicitudDerriboView(LoginRequiredMixin, DetailView):
    model = SolicitudDerribo
    template_name = 'derribo/detalle_solicitud.html'
    context_object_name = 'solicitud'

    def get_queryset(self):
        return SolicitudDerribo.objects.filter(usuario=self.request.user)