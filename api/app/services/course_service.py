from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.course import Course
from app.models.subject import Subject
from app.schemas.course import CourseCreate, CourseUpdate

class CourseService:
    @staticmethod
    def get_courses(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
        return db.query(Course).offset(skip).limit(limit).all()

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
    def create_course(db: Session, course_data: CourseCreate) -> Course:
        subject = db.query(Subject).filter(Subject.id == course_data.subject_id).first()
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asignatura con ID {course_data.subject_id} no encontrada"
            )
        
        course = Course(**course_data.model_dump())
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def update_course(db: Session, course_id: int, course_data: CourseUpdate) -> Course:
        course = CourseService.get_course(db, course_id)
        
        update_data = course_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(course, key, value)
        
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def delete_course(db: Session, course_id: int) -> dict:
        course = CourseService.get_course(db, course_id)
        db.delete(course)
        db.commit()
        return {"message": "Curso eliminado correctamente"}
