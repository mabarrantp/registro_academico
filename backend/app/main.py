from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# ✅ CARGA TODOS LOS MODELOS ANTES DE create_all (evita errores de ForeignKey)
from app.models import _load  # noqa: F401

# ✅ ROUTERS (IMPORT EXPLÍCITO POR ARCHIVO)
from app.routers.auth import router as auth_router
from app.routers.students import router as students_router
from app.routers.enrollments import router as enrollments_router
from app.routers.grades import router as grades_router
from app.routers.subjects import router as subjects_router
from app.routers.quarters import router as quarters_router
from app.routers.assessments import router as assessments_router
from app.routers.quarter_grades import router as quarter_grades_router
from app.routers.final_grades import router as final_grades_router
from app.routers.audit_logs import router as audit_logs_router

app = FastAPI(title="Sistema de Registro Académico", version="0.1.0")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CREAR TABLAS (ya con todos los modelos registrados en metadata)
Base.metadata.create_all(bind=engine)

# ✅ INCLUIR ROUTERS
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(enrollments_router)
app.include_router(grades_router)
app.include_router(subjects_router)
app.include_router(quarters_router)
app.include_router(assessments_router)
app.include_router(quarter_grades_router)
app.include_router(final_grades_router)
app.include_router(audit_logs_router)