"""
Tests para endpoints de estudiantes
"""
import pytest
from fastapi import status


def test_create_student(client, auth_headers):
    response = client.post(
        "/api/v1/students/",
        headers=auth_headers,
        json={
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "juan.perez@university.com"
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["first_name"] == "Juan"
    assert data["last_name"] == "Pérez"
    assert data["email"] == "juan.perez@university.com"
    assert "id" in data


def test_create_student_duplicate_email(client, auth_headers, db_session):
    from app.models.student import Student
    
    student = Student(
        first_name="Existing",
        last_name="Student",
        email="existing@university.com"
    )
    db_session.add(student)
    db_session.commit()
    
    response = client.post(
        "/api/v1/students/",
        headers=auth_headers,
        json={
            "first_name": "Another",
            "last_name": "Student",
            "email": "existing@university.com"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_all_students(client, auth_headers, db_session):
    from app.models.student import Student

    students = [
        Student(first_name="Student1", last_name="Test", email="s1@test.com", student_id="001"),
        Student(first_name="Student2", last_name="Test", email="s2@test.com", student_id="002"),
    ]
    db_session.add_all(students)
    db_session.commit()
    
    response = client.get("/api/v1/students/", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2


def test_get_student_by_id(client, auth_headers, db_session):
    from app.models.student import Student
    
    student = Student(
        first_name="Test",
        last_name="Student",
        email="test.student@university.com",
        student_id="2024050"
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    
    response = client.get(f"/api/v1/students/{student.id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == student.id
    assert data["email"] == "test.student@university.com"


def test_update_student(client, auth_headers, db_session):
    from app.models.student import Student
    
    student = Student(
        first_name="Original",
        last_name="Name",
        email="original@university.com",
        student_id="2024060"
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    
    response = client.put(
        f"/api/v1/students/{student.id}",
        headers=auth_headers,
        json={"first_name": "Updated"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"


def test_delete_student(client, auth_headers, db_session):
    from app.models.student import Student
    
    student = Student(
        first_name="To",
        last_name="Delete",
        email="delete@university.com",
        student_id="2024070"
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    
    response = client.delete(f"/api/v1/students/{student.id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    
    get_response = client.get(f"/api/v1/students/{student.id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
