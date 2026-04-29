from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🔹 Base de datos y modelos
from app.database import Base, engine
import app.models  # 🔴 fuerza la carga de TODOS los modelos (muy importante)

# 🔹 Routers
from app.routers.auth import router as auth_router
from app.routers.students import router as students_router
from app.routers.enrollments import router as enrollments_router
from app.routers.grades import router as grades_router
from app.routers.sections import router as sections_router
from app.routers.teacher_assignments import router as teacher_assignments_router
from app.routers.assessments import router as assessments_router
from app.routers.auth import router as auth_router
from app.routers.dashboard import router as dashboard_router
from app.routers.dashboard_coordination import router as dashboard_coordination_router
from app.routers.dashboard_admin import router as dashboard_admin_router
from app.routers.me import router as me_router
from app.routers.quarter_weights import router as quarter_weights_router
from app.routers.quarters import router as quarters_router
from app.routers.academic_years import router as academic_years_router
from app.routers.report_card import router as report_card_router


# (agrega más routers aquí cuando los tengas)
# from app.routers.subjects import router as subjects_router
# from app.routers.teachers import router as teachers_router

app = FastAPI(
    title="Registro Académico",
    version="1.0.0",
)

# 🔹 CORS (ajusta dominios si luego hace falta)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 CREA TODAS LAS TABLAS (DESARROLLO)
# ⚠️ Esto DEBE ir después de importar app.models
Base.metadata.create_all(bind=engine)

# 🔹 Registro de routers
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(enrollments_router)
app.include_router(grades_router)
app.include_router(sections_router)
app.include_router(teacher_assignments_router)
app.include_router(assessments_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(dashboard_coordination_router)
app.include_router(dashboard_admin_router)
app.include_router(me_router)
app.include_router(quarter_weights_router)
app.include_router(quarters_router)
app.include_router(academic_years_router)
app.include_router(report_card_router)


# (agrega más routers aquí cuando los tengas)   

@app.get("/")
def root():
    return {"status": "Registro Académico activo"}