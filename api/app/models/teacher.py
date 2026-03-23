from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class Teacher(Base):
    __tablename__ = "university_teacher"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    complete_name = Column(String)
    employee_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    active = Column(Boolean, default=True)
    
    # Auditoría Odoo
    create_uid = Column(Integer, default=1)
    write_uid = Column(Integer, default=1)
