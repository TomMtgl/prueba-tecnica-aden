# Prueba Técnica ADEN - Sistema de Gestión Universitaria

Sistema completo de gestión universitaria implementado en dos partes:
- **Parte 1:** Módulo Odoo con gestión académica y administrativa
- **Parte 2:** API REST con FastAPI

## 🚀 Inicio Rápido

### Requisitos Previos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo
- Git

### Instalación

**1. Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/prueba-tecnica-aden.git
cd prueba-tecnica-aden
```

**2. Iniciar Parte 1 - Módulo Odoo:**
```bash
cd parte-1-odoo
docker-compose up -d
```

Espera 1-2 minutos, luego:
- Accede a: http://localhost:8069
- Crea base de datos:
  - Database Name: `university_db`
  - Email: `admin@university.com`
  - Password: `admin`
  - Language: Español
- Ve a **Apps** → Busca **"University"** → Click **Install**

**3. Iniciar Parte 2 - API FastAPI:**
```bash
cd ../parte-2-fastapi
docker-compose up -d
```

Espera 30 segundos, luego:
- Accede a: http://localhost:8000/docs
- Login con: `admin` / `admin123`

### Detener los servicios
```bash
# En cada carpeta
docker-compose down

# Para eliminar también los datos
docker-compose down -v
```

### Menús Invisibles
Si las acciones funcionan por URL pero no ves los menús:
* Verifica que el usuario tenga asignado el grupo **Área Académica** o **Área de Finanzas**.
* Limpia la caché del navegador para forzar la recarga del árbol de menús de Odoo 18.

## ✅ Funcionalidades Implementadas

### Parte 1 - Módulo Odoo

#### Modelos
- ✅ **Estudiantes** con datos personales
- ✅ **Carreras** (Ej: Ingeniería en Sistemas)
- ✅ **Planes de Estudio** por año (Ej: Plan 2024)
- ✅ **Asignaturas** con código, créditos, profesor asignado
- ✅ **Profesores** con información bancaria para pagos
- ✅ **Inscripciones** de estudiantes a asignaturas

#### Funcionalidades Clave
- ✅ **Contador de inscriptos en tiempo real** 
  - Cada asignatura muestra un botón con la cantidad actual de inscriptos
  - Se actualiza automáticamente al agregar/eliminar inscripciones
  
- ✅ **Información de profesores para el área de finanzas**
  - Datos bancarios: Cuenta, Banco, CUIT
  - Sección visible solo para usuarios con rol "Área de Finanzas"
  
- ✅ **Control de acceso por roles:**
  - **Área Académica:** Acceso completo a todo el sistema
  - **Área de Finanzas:** Solo puede ver/editar profesores, NO tiene acceso a inscripciones

#### Datos de Ejemplo
- 2 carreras (Ingeniería en Sistemas, Ingeniería Industrial)
- 2 planes de estudio (2024, 2023)
- 3 asignaturas (Análisis Matemático, Física, Álgebra)
- 2 estudiantes inscriptos
- 2 profesores con información bancaria completa

### Parte 2 - API REST FastAPI

#### Endpoints Principales
- ✅ **Autenticación JWT**
  - `POST /api/v1/auth/register` - Crear usuario
  - `POST /api/v1/auth/login` - Login y obtener token
  - `GET /api/v1/auth/me` - Datos del usuario actual

- ✅ **Estudiantes** (`/api/v1/estudiantes/`)
  - CRUD completo con autenticación
  - Student ID autogenerado (1, 2, 3...)
  - Validación de email único
  
- ✅ **Cursos** (`/api/v1/cursos/`)
  - CRUD completo con autenticación
  - Código único por curso
  - Control de cupo máximo
  
- ✅ **Inscripciones** (`/api/v1/inscripciones/`)
  - Crear inscripción
  - Listar por estudiante o por curso
  - Eliminar inscripción

#### Reglas de Negocio Implementadas
1. ✅ **No duplicados:** Un estudiante NO puede inscribirse dos veces al mismo curso
2. ✅ **Cupo máximo:** Cada curso tiene un límite de inscriptos
3. ✅ **Validación de cupo:** NO se permiten inscripciones si el curso está lleno

#### Soft Delete & Hard Delete
- ✅ **Baja lógica (Soft Delete):**
  - `DELETE /api/v1/estudiantes/{id}/soft`
  - Marca el registro como inactivo (available=false)
  - Mantiene el historial y permite recuperación
  
- ✅ **Restaurar:**
  - `POST /api/v1/estudiantes/{id}/restore`
  - Reactiva un registro dado de baja lógica
  
- ✅ **Baja física (Hard Delete):**
  - `DELETE /api/v1/estudiantes/{id}/hard`
  - Elimina permanentemente de la base de datos
  - ⚠️ Acción IRREVERSIBLE

- ✅ **Filtros:**
  - `GET /api/v1/estudiantes/?include_inactive=false` - Solo activos (default)
  - `GET /api/v1/estudiantes/?include_inactive=true` - Todos

#### Testing
- ✅ Tests de autenticación
- ✅ Tests de CRUD de estudiantes
- ✅ Tests de reglas de negocio en inscripciones
- ✅ Cobertura de casos exitosos y errores

## 📁 Estructura del Proyecto
```
prueba-tecnica-aden/
├── README.md                      # Este archivo
├── .gitignore
│
├── parte-1-odoo/
│   ├── README.md                  # Guía de instalación Odoo
│   ├── docker-compose.yml         # Configuración Docker Odoo
│   └── addons/
│       └── university/            # Módulo personalizado
│           ├── __manifest__.py
│           ├── models/
│           ├── views/
│           ├── security/
│           └── data/
│
└── parte-2-fastapi/
    ├── README.md                  # Guía de instalación API
    ├── docker-compose.yml         # Configuración Docker API
    ├── Dockerfile
    ├── requirements.txt
    ├── .env.example
    ├── main.py
    ├── init_db.py
    ├── app/
    │   ├── models/                # Modelos SQLAlchemy
    │   ├── schemas/               # Schemas Pydantic
    │   ├── services/              # Lógica de negocio
    │   ├── api/v1/endpoints/      # Endpoints REST
    │   ├── core/                  # Config y seguridad
    │   └── db/                    # Configuración BD
    └── tests/                     # Tests automatizados
```

## 🧪 Ejecutar Tests (FastAPI)
```bash
cd parte-2-fastapi
docker-compose exec api pytest -v
```

## 👤 Credenciales

**Odoo:**
- URL: http://localhost:8069
- Usuario: `admin@university.com`
- Password: `admin`

**FastAPI:**
- URL: http://localhost:8000/docs
- Usuario: `admin`
- Password: `admin123`

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.13**
- **FastAPI 0.115.0** - Framework web moderno y rápido
- **Odoo 18.0** - ERP open source
- **SQLAlchemy 2.0** - ORM para Python
- **Pydantic 2.10** - Validación de datos
- **Alembic** - Migraciones de BD

### Base de Datos
- **PostgreSQL 15** - Base de datos relacional

### Autenticación & Seguridad
- **JWT (JSON Web Tokens)** - Autenticación stateless
- **bcrypt** - Hash seguro de contraseñas
- **python-jose** - Manejo de tokens JWT

### Testing
- **pytest** - Framework de testing
- **httpx** - Cliente HTTP para tests

### DevOps
- **Docker & Docker Compose** - Containerización
- **Git** - Control de versiones

## 📊 Arquitectura

### Parte 1 - Odoo
```
Odoo Framework
    ↓
PostgreSQL (puerto 5432)
    ↓
Módulo University
    ├── Models (ORM de Odoo)
    ├── Views (XML)
    └── Security (Grupos y permisos)
```

### Parte 2 - FastAPI
```
Cliente → FastAPI (puerto 8000)
            ↓
         JWT Auth
            ↓
    Endpoints (API Router)
            ↓
      Services (Lógica de negocio)
            ↓
    Models (SQLAlchemy ORM)
            ↓
      PostgreSQL (puerto 5432)
```

## 📝 Notas Técnicas

- Ambos servicios usan PostgreSQL pero en **contenedores separados**
- Los datos persisten en **volúmenes de Docker**
- Hot reload activado en desarrollo (cambios se reflejan automáticamente)
- Documentación interactiva de la API en `/docs` (Swagger)
- Control de acceso basado en roles en Odoo
- Validaciones de negocio implementadas en capa de servicios (FastAPI)

## 🐛 Troubleshooting

### Puerto 8069 ya en uso
```bash
# Detener Odoo
cd parte-1-odoo
docker-compose down
```

### Puerto 8000 ya en uso
```bash
# Detener FastAPI
cd parte-2-fastapi
docker-compose down
```

### Resetear todo (eliminar datos)
```bash
# En cada carpeta
docker-compose down -v
docker-compose up -d
```

### Ver logs en tiempo real
```bash
# Odoo
docker-compose logs -f web

# FastAPI
docker-compose logs -f api
```

## 📧 Contacto

**Desarrollado por:** Tomas Montigel 
**Email:** [montigeltomas@gmail.com]  
**GitHub:** [TomMtgl]

---

**Prueba Técnica ADEN - 2026**