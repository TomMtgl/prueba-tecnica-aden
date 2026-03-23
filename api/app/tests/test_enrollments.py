"""
Tests para endpoints de inscripciones
Incluye validación de reglas de negocio
"""
import pytest
from fastapi import status


@pytest.fixture
def sample_student(db_session):
    from app.models.student import Student
    
    student = Student(
        first_name="Test",
        last_name="Student",
        email="test@university.com",
        student_id="TEST001"
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    return student


@pytest.fixture
def sample_course(db_session):
    from app.models.course import Course
    
    course = Course(
        code="TEST101",
        name="Test Course",
        description="A test course",
        max_capacity=2  
    )
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)
    return course


def test_create_enrollment_success(client, auth_headers, sample_student, sample_course):
    response = client.post(
        "/api/v1/enrollments/",
        headers=auth_headers,
        json={
            "student_id": sample_student.id,
            "course_id": sample_course.id
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["student_id"] == sample_student.id
    assert data["course_id"] == sample_course.id


def test_duplicate_enrollment_fails(client, auth_headers, sample_student, sample_course):
    client.post(
        "/api/v1/enrollments/",
        headers=auth_headers,
        json={
            "student_id": sample_student.id,
            "course_id": sample_course.id
        }
    )
    

    response = client.post(
        "/api/v1/enrollments/",
        headers=auth_headers,
        json={
            "student_id": sample_student.id,
            "course_id": sample_course.id
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "ya está inscrito" in response.json()["detail"]


def test_course_full_prevents_enrollment(client, auth_headers, sample_course, db_session):
    from app.models.student import Student
    

    student1 = Student(first_name="S1", last_name="Test", email="s1@test.com", student_id="S001")
    student2 = Student(first_name="S2", last_name="Test", email="s2@test.com", student_id="S002")
    student3 = Student(first_name="S3", last_name="Test", email="s3@test.com", student_id="S003")
    
    db_session.add_all([student1, student2, student3])
    db_session.commit()
    db_session.refresh(student1)
    db_session.refresh(student2)
    db_session.refresh(student3)
    

    client.post(
        "/api/v1/enrollments/",
        headers=auth_headers,
        json={"student_id": student1.id, "course_id": sample_course.id}
    )
    
    client.post(
        "/api/v1/enrollments/",
        headers=auth_headers,
        json={"student_id": student2.id, "course_id": sample_course.id}
    )
    

    response = client.post(
        "/api/v1/enrollments/",
        headers=auth_headers,
        json={"student_id": student3.id, "course_id": sample_course.id}
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "lleno" in response.json()["detail"]


def test_list_student_enrollments(client, auth_headers, sample_student, db_session):
    from app.models.course import Course
    from app.models.enrollment import Enrollment
    

    course1 = Course(code="C1", name="Course 1", max_capacity=30)
    course2 = Course(code="C2", name="Course 2", max_capacity=30)
    db_session.add_all([course1, course2])
    db_session.commit()
    

    enrollment1 = Enrollment(student_id=sample_student.id, course_id=course1.id)
    enrollment2 = Enrollment(student_id=sample_student.id, course_id=course2.id)
    db_session.add_all([enrollment1, enrollment2])
    db_session.commit()
    

    response = client.get(
        f"/api/v1/enrollments/student/{sample_student.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_list_course_enrollments(client, auth_headers, sample_course, db_session):
    from app.models.student import Student
    from app.models.enrollment import Enrollment
    

    student1 = Student(first_name="S1", last_name="Test", email="st1@test.com", student_id="ST001")
    student2 = Student(first_name="S2", last_name="Test", email="st2@test.com", student_id="ST002")
    db_session.add_all([student1, student2])
    db_session.commit()
    

    enrollment1 = Enrollment(student_id=student1.id, course_id=sample_course.id)
    enrollment2 = Enrollment(student_id=student2.id, course_id=sample_course.id)
    db_session.add_all([enrollment1, enrollment2])
    db_session.commit()
    

    response = client.get(
        f"/api/v1/enrollments/course/{sample_course.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_delete_enrollment(client, auth_headers, sample_student, sample_course, db_session):
    from app.models.enrollment import Enrollment
    

    enrollment = Enrollment(student_id=sample_student.id, course_id=sample_course.id)
    db_session.add(enrollment)
    db_session.commit()
    db_session.refresh(enrollment)
    

    response = client.delete(
        f"/api/v1/enrollments/{enrollment.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    

    get_response = client.get(
        f"/api/v1/enrollments/{enrollment.id}",
        headers=auth_headers
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_enroll_nonexistent_student(client, auth_headers, sample_course):
    response = client.post(
        "/api/v1/enrollments/",
        headers=auth_headers,
        json={
            "student_id": 99999,  # No existe
            "course_id": sample_course.id
        }
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_enroll_nonexistent_course(client, auth_headers, sample_student):
    response = client.post(
        "/api/v1/enrollments/",
        headers=auth_headers,
        json={
            "student_id": sample_student.id,
            "course_id": 99999  # No existe
        }
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
