"""
Modelo de Inscripción (Enrollment)
Representa la relación muchos a muchos entre estudiantes y cursos
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Enrollment(Base):
    
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrollment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='unique_student_course'),
    )
    
    def __repr__(self):
        return f"<Enrollment: Student {self.student_id} - Course {self.course_id}>"
