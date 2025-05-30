from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import random
from typing import List
import os
from dotenv import load_dotenv
from models import MRI, Diagnosis, Patient
from bson import ObjectId
import httpx

load_dotenv()

app = FastAPI(title="Hospital MRI Analysis System")

# Configuración desde variables de entorno
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
EVENTOS_URL = os.getenv("EVENTOS_URL", "http://localhost:8002")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

try:
    client = AsyncIOMotorClient(MONGODB_URL)
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

db = client.hospital_db

# Sample diagnoses for random selection
SAMPLE_DIAGNOSES = [
    "Normal brain MRI, no significant findings",
    "Mild cerebral atrophy",
    "Small white matter lesions",
    "Possible early signs of multiple sclerosis",
    "Normal variant, no pathological findings",
    "Mild ventricular enlargement",
    "Small arachnoid cyst",
    "Normal aging changes",
    "Possible early signs of dementia",
    "Normal brain parenchyma"
]

@app.get("/")
async def root():
    return {"message": "Welcome to Hospital MRI Analysis System"}

@app.post("/mri/upload")
async def upload_mri(
    file: UploadFile = File(...),
    patient_id: str = None
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Save the file
        file_location = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
        
        # Create MRI record
        mri = MRI(
            filename=file.filename,
            upload_date=datetime.now(),
            patient_id=patient_id,
            uploaded_by="system",
            file_path=file_location
        )
        
        # Save to database
        result = await db.mris.insert_one(mri.dict())
        
        # Notify eventos service about new MRI upload
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{EVENTOS_URL}/events",
                    json={
                        "type": "mri_upload",
                        "patient_id": patient_id,
                        "mri_id": str(result.inserted_id),
                        "user_id": "system"
                    }
                )
        except Exception as e:
            print(f"Warning: Could not notify eventos service: {e}")
            # Continue execution even if eventos notification fails
        
        return {"message": "MRI uploaded successfully", "mri_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mri/{mri_id}/analyze")
async def analyze_mri(mri_id: str):
    try:
        mri_object_id = ObjectId(mri_id)
        mri = await db.mris.find_one({"_id": mri_object_id})
        if not mri:
            raise HTTPException(status_code=404, detail="MRI not found")
        
        diagnosis_text = random.choice(SAMPLE_DIAGNOSES)
        
        diagnosis = Diagnosis(
            mri_id=mri_id,
            diagnosis_text=diagnosis_text,
            analysis_date=datetime.now(),
            analyzed_by="system"
        )
        
        result = await db.diagnoses.insert_one(diagnosis.dict())
        
        # Notify eventos service about new diagnosis
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{EVENTOS_URL}/events",
                    json={
                        "type": "mri_diagnosis",
                        "patient_id": mri["patient_id"],
                        "mri_id": mri_id,
                        "diagnosis_id": str(result.inserted_id),
                        "user_id": "system"
                    }
                )
        except Exception as e:
            print(f"Warning: Could not notify eventos service: {e}")
            # Continue execution even if eventos notification fails
        
        return {
            "message": "Analysis completed",
            "diagnosis": diagnosis_text,
            "diagnosis_id": str(result.inserted_id)
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail="Invalid MRI ID format")

@app.get("/mri/{mri_id}/diagnosis")
async def get_diagnosis(mri_id: str):
    try:
        mri_object_id = ObjectId(mri_id)
        diagnosis_doc = await db.diagnoses.find_one({"mri_id": mri_id})
        if not diagnosis_doc:
            raise HTTPException(status_code=404, detail="Diagnosis not found")
        
        diagnosis_doc["_id"] = str(diagnosis_doc["_id"])
        diagnosis = Diagnosis(**diagnosis_doc)
        
        return diagnosis
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail="Invalid MRI ID format")

@app.get("/patient/{patient_id}/mris")
async def get_patient_mris(patient_id: str):
    mris = []
    async for mri_doc in db.mris.find({"patient_id": patient_id}):
        mri_doc["_id"] = str(mri_doc["_id"])
        mri = MRI(**mri_doc)
        mris.append(mri)
    
    return mris

@app.get("/mris")
async def list_all_mris(skip: int = 0, limit: int = 100):
    mris = []
    async for mri_doc in db.mris.find().skip(skip).limit(limit):
        mri_doc["_id"] = str(mri_doc["_id"])
        mri = MRI(**mri_doc)
        mris.append(mri)
    
    total = await db.mris.count_documents({})
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "mris": mris
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT) 