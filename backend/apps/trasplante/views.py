from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import SolicitudTraslado
from .forms import SolicitudTrasladoForm

class CrearSolicitudTrasladoView(LoginRequiredMixin, CreateView):
    model = SolicitudTraslado
    form_class = SolicitudTrasladoForm
    template_name = 'tramites/trasplante.html'
    success_url = reverse_lazy('traslado:lista')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Solicitud de traslado enviada correctamente. Requerirá inspección técnica.'
        )
        return response

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