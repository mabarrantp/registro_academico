from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import defaultdict

from app.database import get_db
from security import get_current_user, require_roles

from models.quarter_grade import QuarterGrade
from models.final_subject_grade import FinalSubjectGrade


router = APIRouter(
    prefix="/final-subject-grades",
    tags=["Final Subject Grades"]
)

PASSING_GRADE = 60


# =====================================================
# CALCULAR NOTAS ANUALES POR MATERIA
# =====================================================
@router.post("/calculate")
def calculate_final_subject_grades(
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Calcula notas anuales por materia.
    NO decide promoción.
    """
    require_roles("ADMIN", "COORDINATION")(user)

    grades = db.query(QuarterGrade).filter(
        QuarterGrade.academic_year == academic_year
    ).all()

    by_student_subject = defaultdict(list)

    for g in grades:
        key = (g.student_id, g.subject_id)
        by_student_subject[key].append(g.final_grade)

    results = {
        "created": 0,
        "updated": 0
    }

    for (student_id, subject_id), values in by_student_subject.items():
        avg = round(sum(values) / len(values), 2)

        status = "PASSED" if avg >= PASSING_GRADE else "REMEDIAL"

        existing = db.query(FinalSubjectGrade).filter(
            FinalSubjectGrade.student_id == student_id,
            FinalSubjectGrade.subject_id == subject_id,
            FinalSubjectGrade.academic_year == academic_year
        ).first()

        if existing:
            existing.final_grade = avg
            existing.status = status
            results["updated"] += 1
        else:
            db.add(FinalSubjectGrade(
                student_id=student_id,
                subject_id=subject_id,
                academic_year=academic_year,
                final_grade=avg,
                status=status
            ))
            results["created"] += 1

    db.commit()
    return results