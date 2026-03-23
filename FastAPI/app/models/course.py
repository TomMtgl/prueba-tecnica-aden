"""
Modelo de Curso
"""
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base


class Course(Base):
    """Modelo de curso/asignatura"""
    
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False) 
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    max_capacity = Column(Integer, nullable=False, default=30)
    available = Column(Boolean, default=True, nullable=False)  
    
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Course {self.code}: {self.name}>"
    
    @property
    def current_enrollment_count(self):
        return len(self.enrollments)
    
    @property
    def is_full(self):
        return self.current_enrollment_count >= self.max_capacity
    
    @property
    def available_spots(self):
        return self.max_capacity - self.current_enrollment_count
