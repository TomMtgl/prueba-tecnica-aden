"""
Servicio de Estudiantes
Contiene la lógica de negocio para operaciones con estudiantes
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    """Servicio para gestión de estudiantes"""
    
    @staticmethod
    def create_student(db: Session, student_data: StudentCreate) -> Student:
        existing_email = db.query(Student).filter(Student.email == student_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un estudiante con el email {student_data.email}"
            )
        
        # Autogenerar student_id 
        if not student_data.student_id:
            last_student = db.query(Student).order_by(Student.id.desc()).first()
            
            if last_student and last_student.student_id.isdigit():
                new_number = int(last_student.student_id) + 1
            else:
                new_number = 1
            
            generated_student_id = str(new_number)
        else:
            generated_student_id = student_data.student_id
        
        try:
            student = Student(
                first_name=student_data.first_name,
                last_name=student_data.last_name,
                email=student_data.email,
                student_id=generated_student_id
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            return student
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear el estudiante. Verifique los datos."
            )
    
    @staticmethod
    def get_student(db: Session, student_id: int) -> Student:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {student_id} no encontrado"
            )
        return student
    
    @staticmethod
    def get_all_students(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
        return db.query(Student).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_student(db: Session, student_id: int, student_data: StudentUpdate) -> Student:
        student = StudentService.get_student(db, student_id)
        
        update_data = student_data.model_dump(exclude_unset=True)
        
        if "email" in update_data:
            existing = db.query(Student).filter(
                Student.email == update_data["email"],
                Student.id != student_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro estudiante con el email {update_data['email']}"
                )
        
        for field, value in update_data.items():
            setattr(student, field, value)
        
        try:
            db.commit()
            db.refresh(student)
            return student
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar el estudiante"
            )


    @staticmethod
    def soft_delete_student(db: Session, student_id: int) -> dict:
        student = StudentService.get_student(db, student_id)
        
        if not student.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estudiante {student.full_name} ya está inactivo"
            )
        
        student.available = False
        db.commit()
        db.refresh(student)
        
        return {
            "message": f"Estudiante {student.full_name} dado de baja (baja lógica)",
            "student_id": student.student_id,
            "active": student.active
        }
    
    @staticmethod
    def restore_student(db: Session, student_id: int) -> dict:
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {student_id} no encontrado"
            )
        
        if student.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estudiante {student.full_name} ya está activo"
            )
        
        student.available = True
        db.commit()
        db.refresh(student)
        
        return {
            "message": f"Estudiante {student.full_name} restaurado exitosamente",
            "student_id": student.student_id,
            "active": student.active
        }
    
    @staticmethod
    def hard_delete_student(db: Session, student_id: int) -> dict:
        student = StudentService.get_student(db, student_id)
        student_info = {
            "full_name": student.full_name,
            "student_id": student.student_id
        }
        
        db.delete(student)
        db.commit()
        
        return {
            "message": f"Estudiante {student_info['full_name']} eliminado permanentemente (baja física)",
            "student_id": student_info['student_id'],
            "warning": "Esta acción es IRREVERSIBLE"
        }
