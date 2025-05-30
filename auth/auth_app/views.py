from django.shortcuts import render
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'home.html')

@login_required
def eventos_view(request):
    return render(request, 'eventos.html')

@login_required
def analisis_view(request):
    return render(request, 'analisis.html')