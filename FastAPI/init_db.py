from app.db.database import SessionLocal, engine, Base
from app.models import User, Student, Course
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
import random

def seed_students(db: Session):
    """Genera 30 alumnos ficticios con datos aleatorios."""
    nombres = ["Lucas", "Ana", "Diego", "Marta", "Julian", "Sofia", "Mateo", "Valentina", "Nicolas", "Elena", "Andrés", "Lucía"]
    apellidos = ["Sosi", "García", "Rodríguez", "López", "Martínez", "González", "Pérez", "Sánchez", "Romero", "Torres"]
    dominios = ["example.com", "university.edu", "mail.com"]

    print(" -> Generando 30 alumnos...")
    
    for i in range(1, 31):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        email = f"{nombre.lower()}.{apellido.lower()}.{i}@example.com"
        
        exists = db.query(Student).filter(Student.email == email).first()
        if not exists:
            nuevo_estudiante = Student(
                first_name=nombre,
                last_name=apellido,
                email=email,
                student_id=f"{i}",
                available=True
            )
            db.add(nuevo_estudiante)
    
    db.commit()
    print(" -> 30 alumnos creados con éxito.")

def init_db():
    print("=== Inicialización de Base de Datos en Neon ===")
    
    print("\n1. Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("   Tablas creadas/verificadas.")
    
    db = SessionLocal()
    
    try:
        print("\n2. Verificando usuario administrador...")
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                email="admin@university.com",
                hashed_password=get_password_hash("admin123"),
                available=True 
            )
            db.add(admin_user)
            db.commit()
            print("   Usuario 'admin' creado (Pass: admin123).")
        else:
            print("   El usuario 'admin' ya existe.")

        print("\n3. Verificando cursos...")
        if db.query(Course).count() == 0:
            cursos_iniciales = [
                Course(code="MAT101", name="Análisis Matemático 1", max_capacity=30, available=True),
                Course(code="PROG101", name="Programación 1", max_capacity=35, available=True),
                Course(code="FIS101", name="Física 1", max_capacity=25, available=True)
            ]
            db.add_all(cursos_iniciales)
            db.commit()
            print("   Cursos base creados.")
        else:
            print("   Ya existen cursos en la base de datos.")

        print("\n4. Verificando alumnos...")
        #conteo_alumnos = db.query(Student).count()
        #if conteo_alumnos == 0:
        seed_students(db)
        #else:
           # print(f"   Ya existen {conteo_alumnos} alumnos, saltando carga masiva.")

        print("\n=== ¡Proceso de inicialización finalizado con éxito! ===")

        db.commit() 
        print("Datos persistidos en la base de datos")

    except Exception as e:
        print(f"\n ERROR CRÍTICO: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()