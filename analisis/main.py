from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import random
from typing import List
import os
from dotenv import load_dotenv
from models import MRI, Diagnosis, Patient
from auth import get_current_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from bson import ObjectId

load_dotenv()

app = FastAPI(title="Hospital MRI Analysis System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL")
if not MONGODB_URL:
    raise ValueError("MONGODB_URL environment variable is not set")

try:
    client = AsyncIOMotorClient(MONGODB_URL)
    # Verify the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
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

# Sample users for demonstration
DEMO_USERS = {
    "doctor1": "password123",
    "doctor2": "password456",
    "radiologist1": "password789", 
    "malu": "malu"
}

@app.get("/")
async def root():
    return {"message": "Welcome to Hospital MRI Analysis System"}

@app.post("/mri/upload")
async def upload_mri(
    file: UploadFile = File(...),
    patient_id: str = None,
    current_user: dict = Depends(get_current_user)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
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
        uploaded_by=current_user["username"]
    )
    
    # Save to database
    result = await db.mris.insert_one(mri.dict())
    
    return {"message": "MRI uploaded successfully", "mri_id": str(result.inserted_id)}

@app.post("/mri/{mri_id}/analyze")
async def analyze_mri(
    mri_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        # Convertir el string ID a ObjectId
        mri_object_id = ObjectId(mri_id)
        
        # Get MRI record
        mri = await db.mris.find_one({"_id": mri_object_id})
        if not mri:
            raise HTTPException(status_code=404, detail="MRI not found")
        
        # Generate random diagnosis
        diagnosis_text = random.choice(SAMPLE_DIAGNOSES)
        
        # Create diagnosis record
        diagnosis = Diagnosis(
            mri_id=mri_id,
            diagnosis_text=diagnosis_text,
            analysis_date=datetime.now(),
            analyzed_by=current_user["username"]
        )
        
        # Save to database
        result = await db.diagnoses.insert_one(diagnosis.dict())
        
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
async def get_diagnosis(
    mri_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        # Convertir el string ID a ObjectId
        mri_object_id = ObjectId(mri_id)
        
        # Buscar el diagnóstico usando el ObjectId
        diagnosis_doc = await db.diagnoses.find_one({"mri_id": mri_id})
        if not diagnosis_doc:
            raise HTTPException(status_code=404, detail="Diagnosis not found")
        
        # Convertir el ObjectId a string para el modelo
        diagnosis_doc["_id"] = str(diagnosis_doc["_id"])
        diagnosis = Diagnosis(**diagnosis_doc)
        
        return diagnosis
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail="Invalid MRI ID format")

@app.get("/patient/{patient_id}/mris")
async def get_patient_mris(
    patient_id: str,
    current_user: dict = Depends(get_current_user)
):
    # Convertir los documentos de MongoDB a nuestros modelos Pydantic
    mris = []
    async for mri_doc in db.mris.find({"patient_id": patient_id}):
        # Convertir el ObjectId a string para el modelo
        mri_doc["_id"] = str(mri_doc["_id"])
        mri = MRI(**mri_doc)
        mris.append(mri)
    
    return mris

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = DEMO_USERS.get(form_data.username)
    if not user or user != form_data.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/mris")
async def list_all_mris(
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Lista todos los MRIs cargados en el sistema con sus IDs.
    Permite paginación usando skip y limit.
    """
    mris = []
    async for mri_doc in db.mris.find().skip(skip).limit(limit):
        # Convertir el ObjectId a string para el modelo
        mri_doc["_id"] = str(mri_doc["_id"])
        mri = MRI(**mri_doc)
        mris.append(mri)
    
    # Obtener el total de documentos
    total = await db.mris.count_documents({})
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "mris": mris
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 