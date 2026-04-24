from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

# ✅ CARGA TODOS LOS MODELOS ANTES DE create_all (evita errores de ForeignKey)
from models import _load  # noqa: F401

# ✅ ROUTERS (IMPORT EXPLÍCITO POR ARCHIVO)
from routers.auth import router as auth_router
from routers.students import router as students_router
from routers.enrollments import router as enrollments_router
from routers.grades import router as grades_router
from routers.subjects import router as subjects_router
from routers.quarters import router as quarters_router
from routers.assessments import router as assessments_router
from routers.quarter_grades import router as quarter_grades_router
from routers.final_grades import router as final_grades_router
from routers.audit_logs import router as audit_logs_router
from routers.grade_policy import router as grade_policies_router  # ✅ NUEVO
from routers.sections import router as sections_router  # <-- NUEVO
from routers.teachers import router as teachers_router
from routers.teacher_assignments import router as teacher_assignments_router
from routers.student_import import router as student_import_router
from routers.import_roster import router as import_roster_router
from routers.reports import router as reports_router




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
app.include_router(grade_policies_router)  # ✅ NUEVO
app.include_router(sections_router)  # <-- NUEVO
app.include_router(teachers_router)
app.include_router(teacher_assignments_router)
app.include_router(student_import_router)
app.include_router(import_roster_router)
app.include_router(reports_router)

