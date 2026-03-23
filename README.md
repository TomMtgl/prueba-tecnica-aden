# Prueba Técnica ADEN - Sistema de Gestión Universitaria

Sistema integral de gestión académica que combina la robustez de un ERP (**Odoo 18**) con la agilidad de una **API REST (FastAPI)**, compartiendo una base de datos centralizada en PostgreSQL.

## 🚀 Inicio Rápido (Despliegue Automático)

### Requisitos Previos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.
- Git.

### Instalación en un solo paso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/prueba-tecnica-aden.git
   cd "Prueba tecnica ADEN"
   ```

2. **Levantar el ecosistema:**
   Desde la raíz, ejecuta:
   ```bash
   docker-compose down -v && docker-compose up -d --build
   ```
   *Este comando limpia volúmenes previos, construye las imágenes e inicializa las bases de datos de forma limpia.*

3. **Acceso a Odoo:**
   - URL: [http://localhost:8069](http://localhost:8069)
   - El sistema creará automáticamente la base de datos `odoo` e instalará el módulo `university`.
   - **Login:** Usuario `admin` / Password `admin`.
   - *Nota: El usuario administrador ya cuenta con todos los permisos universitarios otorgados automáticamente.*

4. **Acceso a la API (FastAPI):**
   - Documentación Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Login API:** `admin` / `admin123` (vía endpoint `/auth/login`).

---

## ✅ Funcionalidades Principales

### Módulo Odoo (Gestión Académica)
- **Modelado Académico Completo**: Carreras, Planes de Estudio (versionados por año), Asignaturas, Profesores, Cursos (Comisiones) y Estudiantes.
- **Asignación de Profesores Inteligente**:
  - Las **Asignaturas** definen qué profesores están calificados para dictarlas.
  - Los **Cursos** filtran automáticamente la lista de docentes para mostrar solo a los calificados para esa materia.
- **Interfaz Odoo 18**: Vistas optimizadas usando el nuevo estándar `<list>`, widgets de estado y contadores en tiempo real.
- **Seguridad Automatizada**: Asignación nativa de grupos de "Administrador Universidad" al usuario admin por defecto.

### API REST FastAPI
- **Autenticación JWT**: Seguridad stateless para el consumo externo de datos.
- **Gestión de Datos**: CRUD completo sincronizado con el esquema de Odoo.
- **Reglas de Negocio en Inscripciones**:
  - Validación de **Cupo Máximo** por curso.
  - Control de **No Duplicidad**: Un estudiante no puede inscribirse dos veces a la misma asignatura.
- **Soft Delete**: Baja lógica de registros para preservar integridad referencial.

---

## 📁 Estructura del Proyecto
```
Prueba tecnica ADEN/
├── docker-compose.yml             # Orquestación de Odoo, API y PostgreSQL
├── api/                           # Backend FastAPI
│   ├── app/
│   │   ├── models/                # Modelos SQLAlchemy (Sync con Odoo)
│   │   ├── services/              # Reglas de negocio
│   │   └── api/v1/                # Endpoints REST
│   └── init_db.py                 # Inicializador de usuarios API
│
└── Odoo/
    └── addons/
        └── university/            # Módulo personalizado
            ├── models/            # Lógica de negocio (Python)
            ├── views/             # Interfaz Odoo 18 (XML)
            ├── security/          # Grupos y Permisos (CSV/XML)
            └── data/              # Datos de prueba y configuración automática
```

## 🧪 Pruebas y Validación

### Ejecutar Tests Automáticos (API)
```bash
docker-compose exec api pytest -v
```

### Datos de Prueba (Demo Data)
El sistema incluye por defecto:
- 2 Carreras (Sistemas e Industrial).
- 3 Profesores especializados.
- 3 Asignaturas con profesores calificados asignados.
- 3 Estudiantes listos para ser inscriptos.

---
**Desarrollado por:** Tomas Montigel
**Prueba Técnica ADEN - 2026**
