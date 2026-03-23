"""
Modelo de Inscripción (Enrollment)
Representa la relación muchos a muchos entre estudiantes y cursos
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base
 
 
class Enrollment(Base):
    
    __tablename__ = "university_enrollment"
    
  
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("university_student.id"), nullable=False)
    career_id = Column(Integer, nullable=True) 
    study_plan_id = Column(Integer, nullable=True) 
    course_id = Column(Integer, ForeignKey("university_course.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("university_subject.id"), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    

    state = Column(String, default='draft', nullable=False)  
    final_grade = Column(Float, nullable=True)  
    
    create_uid = Column(Integer, nullable=True)
    create_date = Column(DateTime, nullable=True)
    write_uid = Column(Integer, nullable=True)
    write_date = Column(DateTime, nullable=True)
    
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    subject = relationship("Subject", back_populates="enrollments")
    
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='unique_student_course'),
    )
    
    def __repr__(self):
        return f"<Inscripcion student_id={self.student_id} course_id={self.course_id}>"
