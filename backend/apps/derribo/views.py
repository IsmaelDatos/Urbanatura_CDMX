from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import SolicitudDerribo
from .forms import SolicitudDerriboForm

class CrearSolicitudDerriboView(LoginRequiredMixin, CreateView):
    model = SolicitudDerribo
    form_class = SolicitudDerriboForm
    template_name = 'tramites/derribo.html'
    success_url = reverse_lazy('derribo:lista')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Solicitud de derribo enviada. Requiere aprobación especial.'
        )
        return response

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