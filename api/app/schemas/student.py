"""
Schemas de Pydantic para Student
Define cómo se validan y serializan los datos
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="Nombre del estudiante")
    last_name: str = Field(..., min_length=1, max_length=100, description="Apellido del estudiante")
    email: EmailStr = Field(..., description="Email del estudiante")
    student_id: Optional[str] = Field(None, max_length=20, description="Matrícula del estudiante")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class StudentResponse(StudentBase):
    id: int
    
    class Config:
        from_attributes = True 


class StudentWithEnrollments(StudentResponse):
    enrollment_count: int = Field(..., description="Cantidad de inscripciones")
    
    class Config:
        from_attributes = True
