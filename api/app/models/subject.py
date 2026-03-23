from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from app.db.database import Base

class Subject(Base):
    __tablename__ = "university_subject"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, index=True, nullable=False)
    study_plan_id = Column(Integer, index=True)
    
    # Campos de Odoo 18 (deben ser String/Selection)
    year = Column(String)
    semester = Column(String)
    
    credits = Column(Integer)
    hours_per_week = Column(Integer)
    active = Column(Boolean, default=True)
    
    # Auditoría Odoo
    create_uid = Column(Integer, default=1)
    write_uid = Column(Integer, default=1)
