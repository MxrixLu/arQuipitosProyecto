from django.urls import path
from . import views
from django.http import HttpResponse
from django.shortcuts import render

urlpatterns = [
    path('<id>', views.ver_historial_medico, name='ver_historial_medico'),
    path('<id>/', views.ver_historial_medico, name='ver_historial_medico'),
    path('', views.solicitar_historial_medico, name='solicitar_historial_medico'),
]