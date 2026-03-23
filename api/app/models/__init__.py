"""
Importa todos los modelos para facilitar su uso
"""
from app.models.user import User
from app.models.student import Student
from app.models.subject import Subject
from app.models.teacher import Teacher
from app.models.course import Course
from app.models.enrollment import Enrollment

__all__ = ["User", "Student", "Subject", "Teacher", "Course", "Enrollment"]
