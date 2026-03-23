"""
Schemas de Pydantic para Course
"""
from pydantic import BaseModel, Field
from typing import Optional


class CourseBase(BaseModel):
    """Schema base de curso"""
    code: str = Field(..., min_length=1, max_length=20, description="Código del curso")
    name: str = Field(..., min_length=1, max_length=200, description="Nombre del curso")
    description: Optional[str] = Field(None, description="Descripción del curso")
    max_capacity: int = Field(..., gt=0, le=500, description="Capacidad máxima del curso")


class CourseCreate(CourseBase):
    """Schema para crear un curso"""
    pass


class CourseUpdate(BaseModel):
    """Schema para actualizar un curso"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    max_capacity: Optional[int] = Field(None, gt=0, le=500)


class CourseResponse(CourseBase):
    """Schema de respuesta con datos del curso"""
    id: int
    current_enrollment_count: int = Field(..., description="Cantidad actual de inscriptos")
    available_spots: int = Field(..., description="Cupos disponibles")
    is_full: bool = Field(..., description="Indica si el curso está lleno")
    
    class Config:
        from_attributes = True
