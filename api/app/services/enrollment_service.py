"""
Servicio de Inscripciones
Contiene la lógica de negocio para inscripciones
Implementa las reglas de negocio especificadas
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List
from datetime import datetime

from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.subject import Subject
from app.models.course import Course
from app.schemas.enrollment import EnrollmentCreate


class EnrollmentService:
    """Servicio para gestión de inscripciones"""
    
    @staticmethod
    def create_enrollment(db: Session, enrollment_data: EnrollmentCreate) -> Enrollment:
        """
        Crea una nueva inscripción
        
        Reglas de negocio:
        1. El estudiante no puede inscribirse dos veces al mismo curso
        2. El curso no debe estar lleno
        
        Raises:
            HTTPException: Si se viola alguna regla de negocio
        """
        student_id = enrollment_data.student_id
        course_id = enrollment_data.course_id
        
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {student_id} no encontrado"
            )
        
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {course_id} no encontrado"
            )
        
        existing_enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id
        ).first()
        
        if existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estudiante {student.complete_name} ya está inscrito en el curso {course.name}"
            )
        
        if course.is_full:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El curso {course.name} está lleno. Capacidad máxima: {course.capacity}"
            )
        
        try:
            enrollment = Enrollment(
                student_id=student_id,
                course_id=course_id,
                subject_id=course.subject_id,
                enrollment_date=datetime.now().date(),
                state='enrolled'
            )
            db.add(enrollment)
            db.commit()
            db.refresh(enrollment)
            return enrollment
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear la inscripción. El estudiante ya está inscrito en este curso."
            )
    
    @staticmethod
    def get_student_enrollments(db: Session, student_id: int) -> List[Enrollment]:
        """
        Obtiene todas las inscripciones de un estudiante
        
        Raises:
            HTTPException: Si no se encuentra el estudiante
        """
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {student_id} no encontrado"
            )
        
        enrollments = db.query(Enrollment).filter(
            Enrollment.student_id == student_id
        ).all()
        
        return enrollments
    
    @staticmethod
    def get_course_enrollments(db: Session, course_id: int) -> List[Enrollment]:
        """
        Obtiene todas las inscripciones de un curso
        
        Raises:
            HTTPException: Si no se encuentra el curso
        """
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {course_id} no encontrado"
            )
        
        enrollments = db.query(Enrollment).filter(
            Enrollment.course_id == course_id
        ).all()
        
        return enrollments
    
    @staticmethod
    def delete_enrollment(db: Session, enrollment_id: int) -> dict:
        """
        Elimina una inscripción
        
        Raises:
            HTTPException: Si no se encuentra la inscripción
        """
        enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inscripción con ID {enrollment_id} no encontrada"
            )
        
        db.delete(enrollment)
        db.commit()
        return {"message": "Inscripción eliminada correctamente"}
    
    @staticmethod
    def get_enrollment(db: Session, enrollment_id: int) -> Enrollment:
        """
        Obtiene una inscripción por su ID
        
        Raises:
            HTTPException: Si no se encuentra la inscripción
        """
        enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inscripción con ID {enrollment_id} no encontrada"
            )
        return enrollment
