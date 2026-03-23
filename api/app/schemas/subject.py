"""
Schemas de Pydantic para Subject
"""
from pydantic import BaseModel, Field
from typing import Optional


class SubjectBase(BaseModel):
    """Schema base de materia"""
    code: str = Field(..., min_length=1, max_length=20, description="Código de la materia")
    name: str = Field(..., min_length=1, max_length=200, description="Nombre de la materia")
    description: Optional[str] = Field(None, description="Descripción de la materia")
    max_capacity: int = Field(..., gt=0, le=500, description="Capacidad máxima de la materia")


class SubjectCreate(SubjectBase):
    """Schema para crear una materia"""
    pass


class SubjectUpdate(BaseModel):
    """Schema para actualizar una materia"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    max_capacity: Optional[int] = Field(None, gt=0, le=500)


class SubjectResponse(SubjectBase):
    """Schema de respuesta con datos de la materia"""
    id: int
    active: bool = Field(..., description="Indica si la materia está activa")
    current_enrollment_count: int = Field(..., description="Cantidad actual de inscriptos")
    available_spots: int = Field(..., description="Cupos disponibles")
    is_full: bool = Field(..., description="Indica si la materia está llena")
    
    class Config:
        from_attributes = True