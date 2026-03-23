"""
Servicio de Cursos
Contiene la lógica de negocio para operaciones con cursos
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


class CourseService:
    
    @staticmethod
    def create_course(db: Session, course_data: CourseCreate) -> Course:
        # Verificar si ya existe un curso con ese código
        existing = db.query(Course).filter(Course.code == course_data.code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un curso con el código {course_data.code}"
            )
        
        try:
            course = Course(**course_data.model_dump())
            db.add(course)
            db.commit()
            db.refresh(course)
            return course
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear el curso. Verifique los datos."
            )
    
    @staticmethod
    def get_course(db: Session, course_id: int) -> Course:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {course_id} no encontrado"
            )
        return course
    
    @staticmethod
    def get_course_by_code(db: Session, code: str) -> Course:
        course = db.query(Course).filter(Course.code == code).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con código {code} no encontrado"
            )
        return course
    
    @staticmethod
    def get_all_courses(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
        """Obtiene todos los cursos con paginación"""
        return db.query(Course).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_course(db: Session, course_id: int, course_data: CourseUpdate) -> Course:
        course = CourseService.get_course(db, course_id)
        
        # Actualizar solo los campos enviados
        update_data = course_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(course, field, value)
        
        try:
            db.commit()
            db.refresh(course)
            return course
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar el curso"
            )
    
    @staticmethod
    def delete_course(db: Session, course_id: int) -> dict:
        course = CourseService.get_course(db, course_id)
        db.delete(course)
        db.commit()
        return {"message": f"Curso {course.name} eliminado correctamente"}
