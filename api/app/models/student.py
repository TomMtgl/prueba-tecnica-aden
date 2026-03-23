from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime
from app.db.database import Base
import datetime

class Student(Base):
    __tablename__ = "university_student"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    complete_name = Column(String)  # Añadido para compatibilidad con Odoo
    email = Column(String, index=True)
    phone = Column(String)
    student_id = Column(String, unique=True, index=True, nullable=False)
    enrollment_date = Column(Date, default=datetime.date.today)
    active = Column(Boolean, default=True)
    
    # Campos de auditoría Odoo
    create_uid = Column(Integer, default=1)
    write_uid = Column(Integer, default=1)
