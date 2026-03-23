from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base

class Course(Base):
    __tablename__ = "university_course"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject_id = Column(Integer, ForeignKey("university_subject.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("university_teacher.id"), nullable=True)
    capacity = Column(Integer, default=30)
    
    create_uid = Column(Integer, nullable=True)
    create_date = Column(DateTime, nullable=True)
    write_uid = Column(Integer, nullable=True)
    write_date = Column(DateTime, nullable=True)

    subject = relationship("Subject", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")

    @property
    def enrolled_count(self):
        return len(self.enrollments)

    @property
    def is_full(self):
        return self.enrolled_count >= self.capacity

    def __repr__(self):
        return f"<Course {self.name}>"
