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
    
    path('generar-imagenes/', views.generar_imagenes, name='generar_imagenes'),
    path('eliminar-imagenes/', views.eliminar_imagenes, name='eliminar_imagenes'),
    path('generar-diagnosticos/', views.generar_diagnosticos_masivos, name='generar_diagnosticos'),
    path('listar-diagnosticos/', views.listar_diagnosticos, name='listar_diagnosticos'),
    path('eliminar-diagnosticos/', views.eliminar_diagnosticos, name='eliminar_diagnosticos'),



    
]