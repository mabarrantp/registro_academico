from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from security import get_current_user, require_roles

from models.quarter_grade import QuarterGrade
from models.student import Student
from models.subject import Subject
from models.quarter import Quarter


router = APIRouter(
    prefix="/quarter-grades",
    tags=["Quarter Grades"]
)

# =====================================================
# LISTAR NOTAS FINALES POR QUARTER
# =====================================================
@router.get("")
def list_quarter_grades(
    student_id: int | None = None,
    subject_id: int | None = None,
    quarter_id: int | None = None,
    academic_year: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Consulta de notas finales ya calculadas.
    NO recalcula nada.
    """
    require_roles("ADMIN", "COORDINATION", "TEACHER")(user)

    query = db.query(QuarterGrade)

    if student_id:
        query = query.filter(QuarterGrade.student_id == student_id)

    if subject_id:
        query = query.filter(QuarterGrade.subject_id == subject_id)

    if quarter_id:
        query = query.filter(QuarterGrade.quarter_id == quarter_id)

    if academic_year:
        query = query.filter(QuarterGrade.academic_year == academic_year)

    grades = query.all()

    return [
        {
            "student_id": g.student_id,
            "subject_id": g.subject_id,
            "quarter_id": g.quarter_id,
            "academic_year": g.academic_year,
            "final_grade": g.final_grade
        }
        for g in grades
    ]