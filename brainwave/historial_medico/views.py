from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import HistorialMedico
import json
from brainwave.auth0backend import getRole
from django.contrib.auth.decorators import login_required


@login_required
def ver_historial_medico(request, id=0): 
    role = getRole(request)
    if role == "Medico":
        historial = HistorialMedico.objects.raw("SELECT * FROM historial_medico_historialmedico WHERE id = %s" % id)[0]
        if not historial:
            messages.error(request, "No se encontró el historial médico.")
            return HttpResponse("Historial no encontrado.", status=404)
        # TODO: Logica para mostrar solo los historiales medicos para paciente que haya atendido el medio
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
        #Dado que solo existen dos roles ["Medico","Admin"] este flujo es para el admin que puede ver todo
        historial = HistorialMedico.objects.raw("SELECT * FROM historial_medico_historialmedico WHERE id = %s" % id)[0]
        if not historial:
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




    