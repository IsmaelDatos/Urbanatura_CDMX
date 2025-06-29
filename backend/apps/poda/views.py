from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import SolicitudPoda
from .forms import SolicitudPodaForm
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect

class CrearSolicitudPodaView(LoginRequiredMixin, CreateView):
    model = SolicitudPoda
    form_class = SolicitudPodaForm
    template_name = "tramites/poda.html"
    success_url = reverse_lazy("poda:lista")

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
                return JsonResponse({"success": True, "message": "Solicitud creada exitosamente"})
            messages.success(self.request, "Solicitud creada exitosamente")
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Error al guardar: {str(e)}")
            return self.form_invalid(form)

class ListaSolicitudesPodaView(LoginRequiredMixin, ListView):
    model = SolicitudPoda
    template_name = 'poda/lista_solicitudes.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        return SolicitudPoda.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')