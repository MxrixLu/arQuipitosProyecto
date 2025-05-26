from eventos.models import Evento, Paciente, Doctor
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
import datetime


def get_eventos():
    print("Connecting to MongoDB...")
    client = MongoClient(settings.MONGO_CLI)
    print("Connected to MongoDB.")
    db = client.eventos_db
    print("Fetching eventos from the database...")
    eventos_collection = db['eventos']
    print(f"Found {eventos_collection.count_documents({})} eventos in the collection.")
    eventos_collection = eventos_collection.find({})
    eventos = [Evento.from_mongo(doc) for doc in eventos_collection]
    client.close()
    
    return eventos