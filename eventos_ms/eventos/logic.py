from eventos.models import Evento, Paciente, Doctor
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
import datetime
from rest_framework.response import Response
from rest_framework import status


def create_evento(data):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        eventos_collection = db['eventos']

        # Verify it paciente_id and doctor_id exist
        if 'paciente_id' in data:
            paciente = db['pacientes'].find_one({'_id': ObjectId(data['paciente_id'])})
            if not paciente:
                return Response({'error': 'Paciente not found'}, status=status.HTTP_404_NOT_FOUND)
        if 'doctor_id' in data:
            doctor = db['doctors'].find_one({'_id': ObjectId(data['doctor_id'])})
            if not doctor:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        
        result = eventos_collection.insert_one(data)
        client.close()
        
        if result.inserted_id:
            return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Failed to create evento'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_eventos():
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        eventos_collection = db['eventos']
        eventos_cursor = eventos_collection.find({})
        eventos = [Evento.from_mongo(doc).to_dict() for doc in eventos_cursor]
        client.close()
        return Response(eventos, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def get_evento_by_id(evento_id):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        eventos_collection = db['eventos']
        
        evento_doc = eventos_collection.find_one({'_id': ObjectId(evento_id)})
        client.close()
        
        if evento_doc:
            evento = Evento.from_mongo(evento_doc)
            return Response(evento.to_dict(), status=status.HTTP_200_OK)
        return Response({'error': 'Evento not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def update_evento(evento_id, data):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        eventos_collection = db['eventos']
        
        result = eventos_collection.update_one({'_id': ObjectId(evento_id)}, {'$set': data})
        client.close()
        
        if result.modified_count > 0:
            return Response({'message': 'Evento updated successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Failed to update evento'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def delete_evento(evento_id):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        eventos_collection = db['eventos']
        
        result = eventos_collection.delete_one({'_id': ObjectId(evento_id)})
        client.close()
        
        if result.deleted_count > 0:
            return Response({'message': 'Evento deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Evento not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_pacientes():
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        pacientes_collection = db['pacientes']
        pacientes_cursor = pacientes_collection.find({})
        pacientes = [Paciente.from_mongo(doc).to_dict() for doc in pacientes_cursor]
        client.close()
        return Response(pacientes, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def get_doctors():
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        doctors_collection = db['doctors']
        doctors_cursor = doctors_collection.find({})
        doctors = [Doctor.from_mongo(doc).to_dict() for doc in doctors_cursor]
        client.close()
        return Response(doctors, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def get_doctor_by_id(doctor_id):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        doctors_collection = db['doctors']
        doctor_doc = doctors_collection.find_one({'_id': ObjectId(doctor_id)})
        client.close()
        if doctor_doc:
            doctor = Doctor.from_mongo(doctor_doc)
            return Response(doctor.to_dict(), status=status.HTTP_200_OK)
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def create_doctor(data):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        doctors_collection = db['doctors']
        
        result = doctors_collection.insert_one(data)
        client.close()
        
        if result.inserted_id:
            return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Failed to create doctor'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def update_doctor(doctor_id, data):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        doctors_collection = db['doctors']

        result = doctors_collection.update_one({'_id': ObjectId(doctor_id)}, {'$set': data})
        client.close()

        if result.modified_count > 0:
            return Response({'message': 'Doctor updated successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Failed to update doctor'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def delete_doctor(doctor_id):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        doctors_collection = db['doctors']

        result = doctors_collection.delete_one({'_id': ObjectId(doctor_id)})
        client.close()

        if result.deleted_count > 0:
            return Response({'message': 'Doctor deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def get_paciente_by_id(paciente_id):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        pacientes_collection = db['pacientes']
        
        paciente_doc = pacientes_collection.find_one({'_id': ObjectId(paciente_id)})
        client.close()
        
        if paciente_doc:
            paciente = Paciente.from_mongo(paciente_doc)
            return Response(paciente.to_dict(), status=status.HTTP_200_OK)
        return Response({'error': 'Paciente not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def create_paciente(data):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        pacientes_collection = db['pacientes']
        
        result = pacientes_collection.insert_one(data)
        client.close()
        
        if result.inserted_id:
            return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Failed to create paciente'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def update_paciente(paciente_id, data):

    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        pacientes_collection = db['pacientes']
        
        result = pacientes_collection.update_one({'_id': ObjectId(paciente_id)}, {'$set': data})
        client.close()
        
        if result.modified_count > 0:
            return Response({'message': 'Paciente updated successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Failed to update paciente'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def delete_paciente(paciente_id):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        pacientes_collection = db['pacientes']
        
        result = pacientes_collection.delete_one({'_id': ObjectId(paciente_id)})
        client.close()
        
        if result.deleted_count > 0:
            return Response({'message': 'Paciente deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Paciente not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def pacientes_of_doctor(doctor_id):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        eventos_collection = db['eventos']
        pacientes_ids = []

        eventos_cursor = eventos_collection.find({'doctor_id': ObjectId(doctor_id)})
        for evento in eventos_cursor:
            if 'paciente_id' in evento and evento['paciente_id'] not in pacientes_ids:
                pacientes_ids.append(evento['paciente_id'])

        client.close()
        return Response(pacientes_ids, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def doctores_of_paciente(paciente_id):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        eventos_collection = db['eventos']
        doctores_ids = []
        pacientes_cursor = eventos_collection.find({'paciente_id': ObjectId(paciente_id)})
        for evento in pacientes_cursor:
            if 'doctor_id' in evento and evento['doctor_id'] not in doctores_ids:
                doctores_ids.append(evento['doctor_id'])

        client.close()
        return Response(doctores_ids, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def eventos_of_paciente(paciente_id):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        eventos_collection = db['eventos']
        
        eventos_cursor = eventos_collection.find({'paciente_id': ObjectId(paciente_id)})
        eventos = [Evento.from_mongo(doc).to_dict() for doc in eventos_cursor]
        
        client.close()
        return Response(eventos, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def eventos_of_doctor(doctor_id):
    try:
        client = MongoClient(settings.MONGO_CLI)
        db = client.eventos_db
        eventos_collection = db['eventos']
        
        eventos_cursor = eventos_collection.find({'doctor_id': ObjectId(doctor_id)})
        eventos = [Evento.from_mongo(doc).to_dict() for doc in eventos_cursor]
        
        client.close()
        return Response(eventos, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)