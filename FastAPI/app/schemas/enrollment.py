"""
Schemas de Pydantic para Enrollment
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class EnrollmentCreate(BaseModel):
    """Schema para crear una inscripción"""
    student_id: int = Field(..., gt=0, description="ID del estudiante")
    course_id: int = Field(..., gt=0, description="ID del curso")


class EnrollmentResponse(BaseModel):
    """Schema de respuesta con datos de la inscripción"""
    id: int
    student_id: int
    course_id: int
    enrollment_date: datetime
    
    class Config:
        from_attributes = True


class EnrollmentDetailResponse(BaseModel):
    """Schema de respuesta detallada con información del estudiante y curso"""
    id: int
    enrollment_date: datetime
    student: dict = Field(..., description="Información del estudiante")
    course: dict = Field(..., description="Información del curso")
    
    class Config:
        from_attributes = True
