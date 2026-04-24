from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.assessment import Assessment
from models.grade_policy import GradePolicy
from models.quarter import Quarter

router = APIRouter(
    prefix="/quarter-grades",
    tags=["Quarter Grades"]
)


@router.post("/calculate")
def calculate_quarter_grade(
    student_id: int,
    subject_id: int,
    grade_id: int,
    quarter_id: int,
    academic_year: int,
    db: Session = Depends(get_db)
):
    # =========================================================
    # 1️⃣ Validar que el quarter exista (solo para las notas)
    # =========================================================
    quarter = (
        db.query(Quarter)
        .filter(
            Quarter.id == quarter_id,
            Quarter.academic_year == academic_year
        )
        .first()
    )

    if not quarter:
        raise HTTPException(status_code=404, detail="Quarter not found")

    # =========================================================
    # 2️⃣ Obtener GradePolicy (❗ SIN quarter_id ❗)
    # =========================================================
    policy = (
        db.query(GradePolicy)
        .filter(
            GradePolicy.subject_id == subject_id,
            GradePolicy.grade_id == grade_id,
            GradePolicy.academic_year == academic_year
        )
        .first()
    )

    if not policy:
        raise HTTPException(status_code=404, detail="GradePolicy not found")

    # =========================================================
    # 3️⃣ Obtener assessments del estudiante para ese quarter
    # =========================================================
    assessments = (
        db.query(Assessment)
        .filter(
            Assessment.student_id == student_id,
            Assessment.subject_id == subject_id,
            Assessment.grade_id == grade_id,
            Assessment.quarter_id == quarter_id,
            Assessment.status == "ACTIVE"
        )
        .all()
    )

    if not assessments:
        raise HTTPException(
            status_code=404,
            detail="No assessments found for this quarter"
        )

    # =========================================================
    # 4️⃣ Agrupar notas por categoría (SIN lazy loading)
    # =========================================================
    # category_id → código
    category_map = {
        1: "QUIZ",
        2: "HOMEWORK",
        3: "CLASSWORK",
        4: "PROJECT",
        5: "TEST",
    }

    categories = {
        "QUIZ": [],
        "HOMEWORK": [],
        "CLASSWORK": [],
        "PROJECT": [],
        "TEST": [],
    }

    for a in assessments:
        code = category_map.get(a.category_id)
        if code:
            categories[code].append(a.score)

    # =========================================================
    # 5️⃣ Función promedio segura
    # =========================================================
    def avg(values):
        return sum(values) / len(values) if values else 0

    # =========================================================
    # 6️⃣ Cálculo final (igual que Excel)
    # =========================================================
    final_score = (
        avg(categories["QUIZ"]) * policy.quiz_weight +
        avg(categories["HOMEWORK"]) * policy.homework_weight +
        avg(categories["CLASSWORK"]) * policy.classwork_weight +
        avg(categories["PROJECT"]) * policy.project_weight +
        avg(categories["TEST"]) * policy.test_weight
    )

    # =========================================================
    # 7️⃣ Respuesta
    # =========================================================
    return {
        "student_id": student_id,
        "subject_id": subject_id,
        "grade_id": grade_id,
        "quarter_id": quarter_id,
        "academic_year": academic_year,
        "final_score": round(final_score, 2)
    }