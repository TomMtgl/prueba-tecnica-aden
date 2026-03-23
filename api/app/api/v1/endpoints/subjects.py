"""
Endpoints para gestión de materias (Subjects)
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectResponse
from app.services.subject_service import SubjectService
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/subjects", tags=["Materias"])


@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea una nueva materia. Requiere autenticación."""
    return SubjectService.create_subject(db, subject_data)


@router.get("/", response_model=List[SubjectResponse])
def get_all_subjects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene la lista de materias activas."""
    return SubjectService.get_all_subjects(db, skip, limit)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene una materia por ID (solo si está activa)."""
    return SubjectService.get_subject(db, subject_id)


@router.get("/code/{subject_code}", response_model=SubjectResponse)
def get_subject_by_code(
    subject_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca una materia activa por su código único."""
    return SubjectService.get_subject_by_code(db, subject_code)


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int,
    subject_data: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza los datos de una materia activa."""
    return SubjectService.update_subject(db, subject_id, subject_data)


@router.delete("/{subject_id}", status_code=status.HTTP_200_OK)
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Realiza una baja lógica desactivando la materia (active = False)."""
    return SubjectService.delete_subject(db, subject_id)


@router.patch("/{subject_id}/restore", response_model=SubjectResponse)
def restore_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Restaura una materia que fue desactivada previamente."""
    return SubjectService.restore_subject(db, subject_id)