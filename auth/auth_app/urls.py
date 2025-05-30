# mi_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('eventos/', views.eventos_view, name='eventos'),
    path('analisis/', views.analisis_view, name='analisis'),
]
