from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import SolicitudDerribo
from .forms import SolicitudDerriboForm
from django.http import JsonResponse
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

class CrearSolicitudDerriboView(LoginRequiredMixin, CreateView):
    model = SolicitudDerribo
    form_class = SolicitudDerriboForm
    template_name = "tramites/derribo.html"
    success_url = reverse_lazy("arbol:inicio")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario"] = self.request.user
        return kwargs

    def form_valid(self, form):
        logger.info("Intentando guardar solicitud de derribo...")
        try:
            self.object = form.save()
            logger.info(f"Solicitud de derribo guardada con ID: {self.object.id}")
            response_data = {
                'success': True,
                'message': 'Solicitud de derribo creada exitosamente',
                'redirect_url': str(self.get_success_url())
            }
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            messages.success(self.request, response_data['message'])
            return redirect(self.get_success_url())
        except Exception as e:
            logger.error(f"Error al guardar la solicitud de derribo: {str(e)}", exc_info=True)
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Error al guardar la solicitud. Por favor verifica los datos.'
                }, status=400)
            messages.error(self.request, 'Error al guardar la solicitud. Por favor verifica los datos.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.warning(f"Formulario inválido. Errores: {form.errors}")
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.get_json_data(),
                'message': 'Por favor corrige los errores en el formulario'
            }, status=400)
        return super().form_invalid(form)

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