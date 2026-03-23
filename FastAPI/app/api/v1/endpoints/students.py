"""
Endpoints para gestión de estudiantes
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.services.student_service import StudentService
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/students", tags=["Estudiantes"])


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crea un nuevo estudiante
    
    Requiere autenticación
    """
    return StudentService.create_student(db, student_data)


@router.get("/", response_model=List[StudentResponse])
def get_all_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene todos los estudiantes
    
    Parámetros:
    - skip: Número de registros a saltar (para paginación)
    - limit: Número máximo de registros a retornar
    
    Requiere autenticación
    """
    return StudentService.get_all_students(db, skip, limit)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene un estudiante por su ID
    
    Requiere autenticación
    """
    return StudentService.get_student(db, student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza un estudiante
    
    Requiere autenticación
    """
    return StudentService.update_student(db, student_id, student_data)


@router.delete("/{student_id}/soft")
def soft_delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StudentService.soft_delete_student(db, student_id)
 
 
@router.post("/{student_id}/restore")
def restore_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StudentService.restore_student(db, student_id)
 
 
@router.delete("/{student_id}/hard")
def hard_delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StudentService.hard_delete_student(db, student_id)
