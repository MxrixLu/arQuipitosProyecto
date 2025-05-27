from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(str(v)):
            raise ValueError("Invalid ObjectId")
        return str(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator):
        return {"type": "string"}

class MRI(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    filename: str
    upload_date: datetime
    patient_id: Optional[str] = None
    uploaded_by: str
    file_path: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class Diagnosis(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    mri_id: str
    diagnosis_text: str
    analysis_date: datetime
    analyzed_by: str
    confidence_score: Optional[float] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class Patient(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    patient_id: str
    name: str
    date_of_birth: datetime
    gender: str
    medical_history: Optional[list] = []
    last_updated: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str} 