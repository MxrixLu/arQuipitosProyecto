from django.shortcuts import render
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
        # Verificar si el médico ha participado en algún evento médico del paciente
        try:
            historial = HistorialMedico.objects.get(id=id)
            eventos_medicos = historial.eventos_medicos.filter(medico=request.user)
            if not eventos_medicos.exists():
                raise HistorialMedico.DoesNotExist
        except HistorialMedico.DoesNotExist:
            messages.error(request, "No se encontró el historial médico o no tiene permiso para verlo.")
            return HttpResponse("Historial no encontrado o acceso denegado.", status=404)
        
        historial_dict = {
            'id': historial.id,
            'created_at': historial.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'paciente': historial.paciente,
            'contraindicaciones': historial.contraindicaciones,
            'diagnostico': historial.diagnostico,
            'tratamiento': historial.tratamiento,
            'seguimiento': historial.seguimiento
        }
        return HttpResponse(json.dumps(historial_dict), content_type='application/json')
    else:
        # Flujo para el admin
        try:
            historial = HistorialMedico.objects.get(id=id)
        except HistorialMedico.DoesNotExist:
            messages.error(request, "No se encontró el historial médico.")
            return HttpResponse("Historial no encontrado.", status=404)
        
        historial_dict = {
            'id': historial.id,
            'created_at': historial.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'paciente': historial.paciente,
            'contraindicaciones': historial.contraindicaciones,
            'diagnostico': historial.diagnostico,
            'tratamiento': historial.tratamiento,
            'seguimiento': historial.seguimiento
        }
        return HttpResponse(json.dumps(historial_dict), content_type='application/json')
    