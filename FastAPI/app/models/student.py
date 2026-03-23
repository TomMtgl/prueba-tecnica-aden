"""
Modelo de Estudiante
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base


class Student(Base):
    """Modelo de estudiante"""
    
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    student_id = Column(String, unique=True, index=True, nullable=False)
    available = Column(Boolean, default=True, nullable=False) 
    
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student {self.student_id}: {self.first_name} {self.last_name}>"
    
    @property
    def full_name(self):
        """Retorna el nombre completo del estudiante"""
        return f"{self.first_name} {self.last_name}"
