from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.services.course_service import CourseService

router = APIRouter(prefix="/courses", tags=["Cursos"])

@router.get("/", response_model=List[CourseResponse])
def get_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtiene todos los cursos"""
    return CourseService.get_courses(db, skip=skip, limit=limit)

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    """Crea un nuevo curso"""
    return CourseService.create_course(db, course_data)

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Obtiene un curso por su ID"""
    return CourseService.get_course(db, course_id)

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db)):
    """Actualiza un curso"""
    return CourseService.update_course(db, course_id, course_data)

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Elimina un curso"""
    return CourseService.delete_course(db, course_id)
