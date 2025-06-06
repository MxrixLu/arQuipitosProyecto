from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import random
import os
from dotenv import load_dotenv
from models import MRI, Diagnosis
from bson import ObjectId
import httpx
from auth.auth0backend import getRole

load_dotenv()

app = FastAPI(title="Hospital MRI Analysis System")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
EVENTOS_URL = os.getenv("EVENTOS_URL", "http://localhost:8002")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# En vez de crear cliente globalmente, lo hacemos en startup
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
    app.db = app.mongodb_client.hospital_db
    # Opcional: hacer ping para verificar conexión
    try:
        await app.mongodb_client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB on startup: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


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

# ----------------------------
# Función para verificar rol
# ----------------------------

async def check_role(request: Request, expected_role: str):
    try:
        role = await getRole(request)
        if role != expected_role:
            raise HTTPException(status_code=403, detail="Access forbidden: insufficient role")
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Role verification failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to Hospital MRI Analysis System"}

@app.post("/mri/upload")
async def upload_mri(file: UploadFile = File(...), patient_id: str = None):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        file_location = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
        
        # Crear registro MRI

        mri = MRI(
            filename=file.filename,
            upload_date=datetime.now(),
            patient_id=patient_id,
            uploaded_by="system",
            file_path=file_location
        )
        
        result = await db.mris.insert_one(mri.dict())
        
        # Notificar al servicio de eventos
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
        

        return {"message": "MRI uploaded successfully", "mri_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mri/{mri_id}/analyze")
async def analyze_mri(mri_id: str):
    try:
        mri_object_id = ObjectId(mri_id)
        mri = await app.db.mris.find_one({"_id": mri_object_id})
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
        
        # Notificar al servicio de eventos
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
async def get_diagnosis(mri_id: str, request: Request):
    await check_role(request, "Medico")
    try:
        mri_object_id = ObjectId(mri_id)
        diagnosis_doc = await app.db.diagnoses.find_one({"mri_id": mri_id})
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
async def get_patient_mris(patient_id: str, request: Request):
    await check_role(request, "Medico")
    mris = []
    async for mri_doc in app.db.mris.find({"patient_id": patient_id}):
        mri_doc["_id"] = str(mri_doc["_id"])
        mri = MRI(**mri_doc)
        mris.append(mri)
    return mris

@app.get("/mris")
async def list_all_mris(skip: int = 0, limit: int = 100, request: Request = None):
    await check_role(request, "Medico")
    mris = []
    async for mri_doc in app.db.mris.find().skip(skip).limit(limit):
        mri_doc["_id"] = str(mri_doc["_id"])
        mri = MRI(**mri_doc)
        mris.append(mri)
    
    total = await app.db.mris.count_documents({})
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "mris": mris
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
