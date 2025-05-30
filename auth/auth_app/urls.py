from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('analisis/', include('analisis.urls')),
    path('eventos/', include('eventos_ms.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('social/', include('social_django.urls')),

]