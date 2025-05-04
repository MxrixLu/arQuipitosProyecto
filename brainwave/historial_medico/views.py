from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from eventos_medicos.models import Examen
from .models import HistorialMedico
import json
from brainwave.auth0backend import getRole
from django.contrib.auth.decorators import login_required


@login_required
def ver_historial_medico(request, id=0): 
    role = getRole(request)
    if role == "Medico":
        try:
            historial = HistorialMedico.objects.get(id=id)
            eventos_medicos = historial.eventos_medicos.filter(medico=request.user)
            if not eventos_medicos.exists():
                raise HistorialMedico.DoesNotExist
        except HistorialMedico.DoesNotExist:
            messages.error(request, "No se encontró el historial médico o no tiene permiso para verlo.")
            return render(request, "historial_medico/error.html", status=404)
        
        return render(request, "historial_medico/ver_historial.html", {"historial": historial})
    else:
        # Flujo para el admin
        try:
            historial = HistorialMedico.objects.get(id=id)
        except HistorialMedico.DoesNotExist:
            messages.error(request, "No se encontró el historial médico.")
            return render(request, "historial_medico/error.html", status=404)
        
        return render(request, "historial_medico/ver_historial.html", {"historial": historial})


@login_required
def solicitar_historial_medico(request):
    return render(request, "historial_medico/solicitar_historial.html")
