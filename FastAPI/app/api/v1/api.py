"""
Router principal que combina todos los endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, students, courses, enrollments


api_router = APIRouter()


api_router.include_router(auth.router)
api_router.include_router(students.router)
api_router.include_router(courses.router)
api_router.include_router(enrollments.router)
