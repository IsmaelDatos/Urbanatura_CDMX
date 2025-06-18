from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import SolicitudPoda
from .forms import SolicitudPodaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class CrearSolicitudPodaView(LoginRequiredMixin, CreateView):
    model = SolicitudPoda
    form_class = SolicitudPodaForm
    template_name = 'tramites/poda.html'
    success_url = reverse_lazy('poda:lista')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Solicitud de poda enviada correctamente')
        return response

class ListaSolicitudesPodaView(LoginRequiredMixin, ListView):
    model = SolicitudPoda
    template_name = 'poda/lista_solicitudes.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        return SolicitudPoda.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')