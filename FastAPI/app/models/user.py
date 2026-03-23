"""
Modelo de Usuario para autenticación
"""
from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base


class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    available = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<User {self.username}>"
