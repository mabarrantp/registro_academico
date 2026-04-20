from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.utils.quarter_guard import ensure_quarter_open
from app.services.quarter_grade_service import calculate_quarter_grade

router = APIRouter(prefix="/quarter-grades", tags=["Quarter Grades"])

# ✅ Decisión B: COORDINATION también puede calcular/recalcular
ALLOWED_ROLES = ("TEACHER", "ADMIN", "COORDINATION")


@router.post("/calculate", dependencies=[Depends(require_roles(*ALLOWED_ROLES))])
def calculate(
    student_id: int,
    subject_id: int,
    grade_id: int,
    quarter_id: int,
    teacher_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
):
    # ✅ No recalcular si el Quarter está cerrado
    ensure_quarter_open(db, quarter_id)

    result = calculate_quarter_grade(
        db=db,
        student_id=student_id,
        subject_id=subject_id,
        grade_id=grade_id,
        quarter_id=quarter_id,
        teacher_id=teacher_id,
        academic_year=academic_year,
    )

    if not result:
        raise HTTPException(status_code=404, detail="GradePolicy not found")

    return {
        "id": result.id,
        "student_id": result.student_id,
        "subject_id": result.subject_id,
        "quarter_id": result.quarter_id,
        "final_score": round(float(result.final_score), 2),
    }