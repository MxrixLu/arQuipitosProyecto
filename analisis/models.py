from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from datetime import datetime
from typing import Optional, Any, Annotated
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {"type": "string"}

class MRI(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    filename: str
    upload_date: datetime
    patient_id: Optional[str] = None
    uploaded_by: str
    file_path: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class Diagnosis(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    mri_id: str
    diagnosis_text: str
    analysis_date: datetime
    analyzed_by: str
    confidence_score: Optional[float] = None

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class Patient(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    patient_id: str
    name: str
    date_of_birth: datetime
    gender: str
    medical_history: Optional[list] = []
    last_updated: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True 