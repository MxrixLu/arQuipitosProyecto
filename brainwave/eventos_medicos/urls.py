from django.urls import path
from . import views
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'eventos_medicos/home.html')

urlpatterns = [
    path('examen/<int:examen_id>/cargar-imagen/', views.cargar_imagen, name='cargar_imagen'),
    path('examen/<int:examen_id>/ver-imagenes/', views.ver_imagenes, name='ver_imagenes'),
    path('resonancias/', views.lista_imagenes_resonancias, name='lista_imagenes_resonancias'),
    path('ver-resonancias/', views.vista_resonancias, name='vista_resonancias'),
    path('generar-imagenes/', views.generar_imagenes, name='generar_imagenes'),
    path('eliminar-imagenes/', views.eliminar_imagenes, name='eliminar_imagenes'),
    path('generar-diagnosticos/', views.generar_diagnosticos_masivos, name='generar_diagnosticos'),
    path('diagnosticos/', views.ListaDiagnosticosView.as_view(), name='lista_diagnosticos'),
    path('eliminar-diagnosticos/', views.eliminar_diagnosticos, name='eliminar_diagnosticos'),
    path("", home, name="home"),  # Página de inicio
]
