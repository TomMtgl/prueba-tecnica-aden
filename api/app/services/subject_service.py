"""
Servicio de Materias
Contiene la lógica de negocio para operaciones con materias (subjects)
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List

from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectUpdate


class SubjectService:
    
    @staticmethod
    def create_subject(db: Session, subject_data: SubjectCreate) -> Subject:
        # Verificar si ya existe una materia con ese código
        existing = db.query(Subject).filter(Subject.code == subject_data.code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una materia con el código {subject_data.code}"
            )
        
        try:
            subject = Subject(**subject_data.model_dump())
            db.add(subject)
            db.commit()
            db.refresh(subject)
            return subject
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear la materia. Verifique los datos."
            )
    
    @staticmethod
    def get_subject(db: Session, subject_id: int, include_inactive: bool = False) -> Subject:
        query = db.query(Subject).filter(Subject.id == subject_id)
        
        if not include_inactive:
            query = query.filter(Subject.active == True)
            
        subject = query.first()
        if not subject:
            detail = "Materia no encontrada o está inactiva"
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        return subject
    
    @staticmethod
    def get_subject_by_code(db: Session, code: str) -> Subject:
        subject = db.query(Subject).filter(Subject.code == code).first()
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Materia con código {code} no encontrada"
            )
        return subject
    
    @staticmethod
    def get_all_subjects(db: Session, skip: int = 0, limit: int = 100) -> List[Subject]:
        """Obtiene solo las materias activas"""
        return db.query(Subject).filter(Subject.active == True).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_subject(db: Session, subject_id: int, subject_data: SubjectUpdate) -> Subject:
        subject = SubjectService.get_subject(db, subject_id)
        
        update_data = subject_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(subject, field, value)
        
        try:
            db.commit()
            db.refresh(subject)
            return subject
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar la materia"
            )
    

    @staticmethod
    def soft_delete_subject(db: Session, subject_id: int) -> dict:
        subject = SubjectService.get_subject(db, subject_id)
        
        subject.active = False
        try:
            db.commit()
            db.refresh(subject)
            return {"message": f"Materia {subject.name} desactivada (baja lógica) correctamente"}
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error al procesar la baja lógica")

    @staticmethod
    def restore_subject(db: Session, subject_id: int) -> Subject:
        subject = SubjectService.get_subject(db, subject_id, include_inactive=True)
        
        if subject.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="La materia ya se encuentra activa"
            )
            
        subject.active = True
        try:
            db.commit()
            db.refresh(subject)
            return subject
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error al restaurar la materia")

    @staticmethod
    def delete_subject(db: Session, subject_id: int) -> dict:
        subject = SubjectService.get_subject(db, subject_id)
        db.delete(subject)
        db.commit()
        return {"message": f"Materia {subject.name} eliminada correctamente"}