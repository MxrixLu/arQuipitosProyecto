import eventos.logic as logic
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def eventos(request):
    try:
        if request.method == 'GET':
            return logic.get_eventos()
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            return logic.create_evento(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
def evento_detail(request, evento_id):
    try:
        if request.method == 'GET':
            return logic.get_evento_by_id(evento_id)
        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            return logic.update_evento(evento_id, data)
        elif request.method == 'DELETE':
            return logic.delete_evento(evento_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def pacientes(request):
    try:
        if request.method == 'GET':
            return logic.get_pacientes()
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            return logic.create_paciente(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
def paciente_detail(request, paciente_id):
    try:
        if request.method == 'GET':
            return logic.get_paciente_by_id(paciente_id)
        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            return logic.update_paciente(paciente_id, data)
        elif request.method == 'DELETE':
            return logic.delete_paciente(paciente_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def doctores(request):
    try:
        if request.method == 'GET':
            return logic.get_doctors()
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            return logic.create_doctor(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
def doctor_detail(request, doctor_id):
    try:
        if request.method == 'GET':
            return logic.get_doctor_by_id(doctor_id)
        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            return logic.update_doctor(doctor_id, data)
        elif request.method == 'DELETE':
            return logic.delete_doctor(doctor_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def doctores_by_paciente(request, paciente_id):
    try:
        if request.method == 'GET':
            return logic.doctores_of_paciente(paciente_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def pacientes_by_doctor(request, doctor_id):
    try:
        if request.method == 'GET':
            return logic.pacientes_of_doctor(doctor_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_eventos_by_paciente(request, paciente_id):
    try:
        if request.method == 'GET':
            return logic.get_eventos_by_paciente(paciente_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_eventos_by_doctor(request, doctor_id):
    try:
        if request.method == 'GET':
            return logic.get_eventos_by_doctor(doctor_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)