from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func

from app.database import get_db
from app.security import get_current_user
from app.models.assessment import Assessment
from app.models.teacher_assignment import TeacherAssignment
from app.models.quarter import Quarter
from app.models.quarter_weight import QuarterWeight
from app.models.student import Student


router = APIRouter(
    prefix="/grades",
    tags=["Grades"],
)


# -------------------------------------------------
# ✅ GET: GRADES consolidado (solo lectura)
# -------------------------------------------------
@router.get("")
def get_grades(
    assignment_id: int = Query(...),
    quarter_id: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 🔒 Acceso: docente, coordinación, admin
    if user.role not in ("TEACHER", "ADMIN", "COORDINATION"):
        raise HTTPException(status_code=403, detail="No autorizado")

    assignment = (
        db.query(TeacherAssignment)
        .filter(TeacherAssignment.id == assignment_id)
        .first()
    )
    if not assignment:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    quarter = db.query(Quarter).filter(Quarter.id == quarter_id).first()
    if not quarter:
        raise HTTPException(status_code=404, detail="Quarter no encontrado")

    weights_row = (
        db.query(QuarterWeight)
        .filter(
            QuarterWeight.quarter_id == quarter_id,
            QuarterWeight.subject_id == assignment.subject_id,
            QuarterWeight.section_id == assignment.section_id,
        )
        .first()
    )
    if not weights_row:
        raise HTTPException(
            status_code=400,
            detail="No hay ponderaciones definidas para este quarter",
        )

    weights = weights_row.weights

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

    grades = []

    for student in students:
        row = {
            "student_id": student.id,
            "student_name": f"{student.first_name} {student.last_name}",
        }

        final_grade = 0.0

        for assessment_type, weight in weights.items():
            avg_score = (
                db.query(func.avg(Assessment.score))
                .filter(
                    Assessment.teacher_assignment_id == assignment_id,
                    Assessment.quarter == quarter_id,
                    Assessment.student_id == student.id,
                    Assessment.assessment_type == assessment_type,
                )
                .scalar()
            )

            avg_score = round(avg_score, 2) if avg_score else 0
            row[assessment_type] = avg_score
            final_grade += (avg_score * weight) / 100

        row["FINAL_GRADE"] = round(final_grade, 2)
        grades.append(row)

    return {
        "assignment": f"{assignment.subject_id} – {assignment.section_id}",
        "quarter": quarter.code,
        "weights": weights,
        "grades": grades,
    }
