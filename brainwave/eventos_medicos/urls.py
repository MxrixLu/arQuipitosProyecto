# eventos_medicos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URL para cargar imágenes de resonancia
    path('examen/<int:examen_id>/cargar-imagen/', views.cargar_imagen, name='cargar_imagen'),

    # URL para ver imágenes de un examen
    path('examen/<int:examen_id>/ver-imagenes/', views.ver_imagenes, name='ver_imagenes'),
    
    path('resonancias/', views.lista_imagenes_resonancias, name='lista_imagenes_resonancias'),
    
    path('ver-resonancias/', views.vista_resonancias, name='vista_resonancias'),
    
    path('health-check/', views.healthCheck),
]