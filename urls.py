# proyecto/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mi_app.urls')),  # tu app principal, si es la que maneja la raíz
    path('eventos/', include('eventos_ms.urls')),
    path('analisis/', include('analisis.urls')),
    path('auth/', include('django.contrib.auth.urls')),  # para login/logout
    path('social/', include('social_django.urls')),  # para login con redes
]
