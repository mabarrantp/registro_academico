from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from security import get_current_user, require_roles

from models.remedial_exam import RemedialExam
from models.final_subject_grade import FinalSubjectGrade


router = APIRouter(
    prefix="/remedials",
    tags=["Remedial Exams"]
)

PASSING_GRADE = 60


# =====================================================
# REGISTRAR EXAMEN DE REPARACIÓN
# =====================================================
@router.post("")
def register_remedial_exam(
    student_id: int,
    subject_id: int,
    academic_year: int,
    score: float,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Registra el examen de reparación de una materia.
    """
    require_roles("ADMIN", "COORDINATION")(user)

    # -------------------------
    # Validar materia en REMEDIAL
    # -------------------------
    fsg = db.query(FinalSubjectGrade).filter(
        FinalSubjectGrade.student_id == student_id,
        FinalSubjectGrade.subject_id == subject_id,
        FinalSubjectGrade.academic_year == academic_year
    ).first()

    if not fsg:
        raise HTTPException(status_code=404, detail="Final subject grade not found")

    if fsg.status != "REMEDIAL":
        raise HTTPException(
            status_code=400,
            detail="La materia no está en estado REMEDIAL"
        )

    # -------------------------
    # Guardar / actualizar examen
    # -------------------------
    existing = db.query(RemedialExam).filter(
        RemedialExam.student_id == student_id,
        RemedialExam.subject_id == subject_id,
        RemedialExam.academic_year == academic_year
    ).first()

    if existing:
        existing.score = score
    else:
        db.add(RemedialExam(
            student_id=student_id,
            subject_id=subject_id,
            academic_year=academic_year,
            score=score
        ))

    # -------------------------
    # Actualizar estado de la materia
    # -------------------------
    if score >= PASSING_GRADE:
        fsg.status = "PASSED_REMEDIAL"
    else:
        fsg.status = "FAILED"

    db.commit()

    return {
        "student_id": student_id,
        "subject_id": subject_id,
        "academic_year": academic_year,
        "score": score,
        "status": fsg.status
    }
