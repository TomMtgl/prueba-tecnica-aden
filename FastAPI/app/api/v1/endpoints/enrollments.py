"""
Endpoints para gestión de inscripciones
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse, EnrollmentDetailResponse
from app.services.enrollment_service import EnrollmentService
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/enrollments", tags=["Inscripciones"])


@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Inscribe un estudiante en un curso
    
    Reglas de negocio:
    - Un estudiante no puede inscribirse dos veces al mismo curso
    - El curso no debe estar lleno
    
    Requiere autenticación
    """
    return EnrollmentService.create_enrollment(db, enrollment_data)


@router.get("/student/{student_id}", response_model=List[EnrollmentDetailResponse])
def get_student_enrollments(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todas las inscripciones de un estudiante
    
    Requiere autenticación
    """
    enrollments = EnrollmentService.get_student_enrollments(db, student_id)
    
    # Formatear la respuesta con detalles
    result = []
    for enrollment in enrollments:
        result.append({
            "id": enrollment.id,
            "enrollment_date": enrollment.enrollment_date,
            "student": {
                "id": enrollment.student.id,
                "full_name": enrollment.student.full_name,
                "email": enrollment.student.email,
                "student_id": enrollment.student.student_id
            },
            "course": {
                "id": enrollment.course.id,
                "code": enrollment.course.code,
                "name": enrollment.course.name,
                "description": enrollment.course.description
            }
        })
    
    return result


@router.get("/course/{course_id}", response_model=List[EnrollmentDetailResponse])
def get_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todas las inscripciones de un curso
    
    Útil para ver cuántos estudiantes están inscritos
    
    Requiere autenticación
    """
    enrollments = EnrollmentService.get_course_enrollments(db, course_id)
    
    # Formatear la respuesta con detalles
    result = []
    for enrollment in enrollments:
        result.append({
            "id": enrollment.id,
            "enrollment_date": enrollment.enrollment_date,
            "student": {
                "id": enrollment.student.id,
                "full_name": enrollment.student.full_name,
                "email": enrollment.student.email,
                "student_id": enrollment.student.student_id
            },
            "course": {
                "id": enrollment.course.id,
                "code": enrollment.course.code,
                "name": enrollment.course.name,
                "description": enrollment.course.description
            }
        })
    
    return result


@router.delete("/{enrollment_id}")
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Elimina una inscripción (des-inscribe a un estudiante de un curso)
    
    Requiere autenticación
    """
    return EnrollmentService.delete_enrollment(db, enrollment_id)


@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene una inscripción por su ID
    
    Requiere autenticación
    """
    return EnrollmentService.get_enrollment(db, enrollment_id)
