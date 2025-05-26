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
        eventos_collection = eventos_collection.find({})
        eventos = [Evento.from_mongo(doc) for doc in eventos_collection]
        client.close()
        return Response(eventos, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)