"""
Configuración de la aplicación FastAPI
Maneja variables de entorno y configuraciones generales
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración general de la aplicación"""
    
    APP_NAME: str = "University API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Ejemplo: postgresql://user:password@host/database
    DATABASE_URL: str = "postgresql://user:password@host/dbname"
    
    SECRET_KEY: str = "tu-clave-super-secreta-cambiar-en-produccion-12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
