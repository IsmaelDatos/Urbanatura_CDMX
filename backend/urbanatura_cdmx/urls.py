from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.usuarios.views import home_ciudadano, home_institucion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.arbol.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('poda/', include('apps.poda.urls', namespace='poda')),
    path('derribo/', include('apps.derribo.urls', namespace='derribo')),
    path('trasplante/', include('apps.trasplante.urls', namespace='trasplante')),
    path('home/ciudadano/', home_ciudadano, name='home_ciudadano'),
    path('home/institucion/', home_institucion, name='home_institucion'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)