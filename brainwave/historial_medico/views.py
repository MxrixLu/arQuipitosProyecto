from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import HistorialMedico
import json
from brainwave.auth0backend import getRole


@login_required
def ver_historial_medico(request, id=0):
    role = getRole(request)
    if role != "Medico":
        return HttpResponse("Unauthorized User", status=403)

    try:
        historial = get_object_or_404(HistorialMedico, id=id)
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
    except Exception as e:
        return HttpResponse(f"Error interno: {str(e)}", status=500)
    
@login_required
def ver_todo_historial(request):
    role = getRole(request)
    if role == "Administrador hospital":
        historial_list = list(HistorialMedico.objects.raw("SELECT * FROM historial_medico_historialmedico"))
        if not historial_list:
            messages.error(request, "No se encontró el historial médico.")
            return HttpResponse("Historial no encontrado.", status=404)
        
        historial_dicts = []
        for h in historial_list:
            historial_dicts.append({
                'id': h.id,
                'created_at': h.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'paciente': h.paciente,
                'contraindicaciones': h.contraindicaciones,
                'diagnostico': h.diagnostico,
                'tratamiento': h.tratamiento,
                'seguimiento': h.seguimiento
            })

        return HttpResponse(json.dumps(historial_dicts), content_type='application/json')
    else:
        return HttpResponse("Unauthorized User", status=403)
    




    