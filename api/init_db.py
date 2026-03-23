from app.db.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
import sqlalchemy as sa
import time

def init_db():
    print("=== Inicialización Segura de la API ===")
    
    # Solo intentamos crear la tabla 'users' que es propia de la API
    # Las demás las dejamos a cargo de Odoo para evitar conflictos de FK
    try:
        User.__table__.create(bind=engine, checkfirst=True)
        print("   [OK] Tabla 'users' verificada/creada.")
    except Exception as e:
        print(f"   [AVISO] No se pudo crear la tabla users (posiblemente ya existe): {e}")

    db = SessionLocal()
    try:
        # Esperar a que la base de datos esté lista
        max_retries = 5
        for i in range(max_retries):
            try:
                # Solo inicializamos el usuario Admin de la API
                if not db.query(User).filter(User.username == "admin").first():
                    db.add(User(
                        username="admin", 
                        email="admin@university.com", 
                        hashed_password=get_password_hash("admin123"),
                        available=True
                    ))
                    db.commit()
                    print("   [OK] Usuario Admin de la API creado.")
                break
            except Exception as e:
                print(f"   [...] Esperando DB ({i+1}/{max_retries})")
                db.rollback()
                time.sleep(5)
        
        print("=== API Lista ===")
    except Exception as e:
        print(f"ERROR en init_db: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
