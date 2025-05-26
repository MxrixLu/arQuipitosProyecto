from eventos.models import Evento, Paciente, Doctor
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
import datetime


def get_eventos():
    client = MongoClient(settings.MONGO_CLI)
    db = client.eventos_db
    eventos_collection = db['eventos']
    eventos_collection = eventos_collection.find({})
    eventos = [Evento.from_mongo(doc) for doc in eventos_collection]
    client.close()
    
    return eventos