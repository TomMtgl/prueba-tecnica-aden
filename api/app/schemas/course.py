from pydantic import BaseModel, Field
from typing import Optional, List

class CourseBase(BaseModel):
    name: str = Field(..., description="Nombre del curso")
    subject_id: int = Field(..., description="ID de la asignatura")
    capacity: int = Field(30, description="Cupo máximo de alumnos")

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    subject_id: Optional[int] = None
    capacity: Optional[int] = None

class CourseResponse(CourseBase):
    id: int
    enrolled_count: int = 0
    
    class Config:
        from_attributes = True
