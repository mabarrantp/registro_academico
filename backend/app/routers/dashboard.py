from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import get_db
from app.security import get_current_user
from app.models.teacher_assignment import TeacherAssignment
from app.models.assessment import Assessment
from app.models.quarter import Quarter
from app.models.student import Student
from app.models.quarter_weight import QuarterWeight


router = APIRouter(
    prefix="/dashboard/teacher",
    tags=["Dashboard - Teacher"],
)


# -------------------------------------------------
# ✅ Helper: calcular promedio ponderado por estudiante
# -------------------------------------------------
def calculate_weighted_average(
    db: Session,
    assignment_id: int,
    quarter_id: int,
    student_id: int,
    weights: dict,
):
    total = 0.0

    for assessment_type, weight in weights.items():
        avg_score = (
            db.query(func.avg(Assessment.score))
            .filter(
                Assessment.teacher_assignment_id == assignment_id,
                Assessment.quarter == quarter_id,
                Assessment.student_id == student_id,
                Assessment.assessment_type == assessment_type,
            )
            .scalar()
        )

        if avg_score is None:
            avg_score = 0

        total += (avg_score * weight) / 100

    return round(total, 2)


# -------------------------------------------------
# ✅ GET: Dashboard por quarter (RESULTADOS ACCIONABLES)
# -------------------------------------------------
@router.get("/quarter/{quarter_id}")
def dashboard_by_quarter(
    quarter_id: int,
    assignment_id: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Solo docentes")

    assignment = (
        db.query(TeacherAssignment)
        .filter(
            TeacherAssignment.id == assignment_id,
            TeacherAssignment.teacher_id == user.teacher_id,
        )
        .first()
    )
    if not assignment:
        raise HTTPException(status_code=403, detail="Asignación no válida")

    quarter = db.query(Quarter).filter(Quarter.id == quarter_id).first()
    if not quarter:
        raise HTTPException(status_code=404, detail="Quarter no encontrado")

    # ✅ Obtener ponderaciones
    qw = (
        db.query(QuarterWeight)
        .filter(
            QuarterWeight.quarter_id == quarter_id,
            QuarterWeight.subject_id == assignment.subject_id,
            QuarterWeight.section_id == assignment.section_id,
        )
        .first()
    )

    if not qw:
        return {
            "quarter": quarter.code,
            "status": quarter.status,
            "top_students": [],
            "students_at_risk": [],
            "all_students": [],
            "message": "No hay ponderaciones definidas para este quarter",
        }

    weights = qw.weights

    # ✅ Obtener estudiantes evaluados en esta asignación
    students = (
        db.query(Student)
        .join(Assessment, Assessment.student_id == Student.id)
        .filter(
            Assessment.teacher_assignment_id == assignment_id,
            Assessment.quarter == quarter_id,
        )
        .distinct()
        .all()
    )

    all_students = []

    for student in students:
        avg = calculate_weighted_average(
            db,
            assignment_id,
            quarter_id,
            student.id,
            weights,
        )

        all_students.append(
            {
                "student_id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "average": avg,
            }
        )

    # ✅ Ordenar por promedio descendente
    all_students.sort(key=lambda x: x["average"], reverse=True)

    # ✅ Clasificar
    top_students = [s for s in all_students if s["average"] >= 90]
    students_at_risk = [s for s in all_students if s["average"] < 60]

    return {
        "quarter": quarter.code,
        "status": quarter.status,
        "top_students": top_students,
        "students_at_risk": students_at_risk,
        "all_students": all_students,
    }

from sqlalchemy.orm import Session
