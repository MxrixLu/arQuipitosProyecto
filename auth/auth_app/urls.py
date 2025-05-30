from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('', include('analisis.urls')),
    path('', include('eventos_ms.urls')),
    path(r'', include('django.contrib.auth.urls')),
    path(r'', include('social_django.urls')),
     path('', views.home, name='home'),
    path('eventos/', views.eventos_view, name='eventos'),
    path('analisis/', views.analisis_view, name='analisis'),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]