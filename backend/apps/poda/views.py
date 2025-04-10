from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import SolicitudPodaForm

def solicitar_poda(request):
    if request.method == 'POST':
        form = SolicitudPodaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SolicitudPodaForm()
    return render(request, 'poda/solicitar_poda.html', {'form': form})
