from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import Base, engine
import app.models  # fuerza la carga de todos los modelos

# Routers
from app.routers.auth import router as auth_router
from app.routers.students import router as students_router
from app.routers.enrollments import router as enrollments_router
from app.routers.grades import router as grades_router
from app.routers.sections import router as sections_router
from app.routers.teacher_assignments import router as teacher_assignments_router
from app.routers.assessments import router as assessments_router
from app.routers.dashboard import router as dashboard_router
from app.routers.dashboard_coordination import router as dashboard_coordination_router
from app.routers.dashboard_admin import router as dashboard_admin_router
from app.routers.me import router as me_router
from app.routers.quarter_weights import router as quarter_weights_router
from app.routers.quarters import router as quarters_router
from app.routers.academic_years import router as academic_years_router
from app.routers.report_card import router as report_card_router
from app.routers.academic_closure import router as academic_closure_router

ENV = os.getenv("ENV", "development")

app = FastAPI(
    title="Registro Académico",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ SOLO EN DESARROLLO
if ENV == "development":
    Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(enrollments_router)
app.include_router(grades_router)
app.include_router(sections_router)
app.include_router(teacher_assignments_router)
app.include_router(assessments_router)
app.include_router(dashboard_router)
app.include_router(dashboard_coordination_router)
app.include_router(dashboard_admin_router)
app.include_router(me_router)
app.include_router(quarter_weights_router)
app.include_router(quarters_router)
app.include_router(academic_years_router)
app.include_router(report_card_router)
app.include_router(academic_closure_router)

@app.get("/")
def root():
    return {"status": "Registro Académico activo"}
