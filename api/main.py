"""
Aplicación principal FastAPI
Universidad API - Sistema de gestión de inscripciones
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    API para gestión de inscripciones universitarias
    
    ## Características
    
    * **Autenticación JWT**: Sistema seguro de autenticación
    * **Gestión de Estudiantes**: CRUD completo de estudiantes
    * **Gestión de Cursos**: CRUD completo de cursos
    * **Inscripciones**: Sistema de inscripción con validaciones de negocio
    
    ## Reglas de Negocio
    
    1. Un estudiante no puede inscribirse dos veces al mismo curso
    2. Un curso tiene cupo máximo
    3. Si el curso está lleno, no se permiten nuevas inscripciones
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Universidad API - Sistema de gestión de inscripciones",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Endpoint para verificar que la API está funcionando"""
    return {"status": "healthy", "version": settings.APP_VERSION}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
