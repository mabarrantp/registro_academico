from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.assessment import Assessment
from models.quarter import Quarter
from security import get_current_user, require_roles

router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"]
)

# =====================================================
# CREATE ASSESSMENT
# =====================================================
@router.post("/")
def create_assessment(
    student_id: int,
    subject_id: int,
    teacher_id: int,
    grade_id: int,
    quarter_id: int,
    category_id: int,
    score: float,
    academic_year: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    # 🔒 SOLO TEACHER / ADMIN / COORDINATION
    require_roles("TEACHER", "ADMIN", "COORDINATION")(user)

    # 🔒 VALIDAR QUARTER
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

    if quarter.status != "OPEN":
        raise HTTPException(
            status_code=403,
            detail="This quarter is closed. You cannot add assessments."
        )

    assessment = Assessment(
        student_id=student_id,
        subject_id=subject_id,
        teacher_id=teacher_id,
        grade_id=grade_id,
        quarter_id=quarter_id,
        category_id=category_id,
        score=score,
        on_time=True,
        status="ACTIVE"
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment


# =====================================================
# UPDATE ASSESSMENT
# =====================================================
@router.put("/{assessment_id}")
def update_assessment(
    assessment_id: int,
    score: float,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    require_roles("TEACHER", "ADMIN", "COORDINATION")(user)

    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    quarter = (
        db.query(Quarter)
        .filter(Quarter.id == assessment.quarter_id)
        .first()
    )

    if quarter.status != "OPEN":
        raise HTTPException(
            status_code=403,
            detail="This quarter is closed. You cannot modify assessments."
        )

    assessment.score = score
    db.commit()

    return assessment


# =====================================================
# LIST ASSESSMENTS
# =====================================================
@router.get("/")
def list_assessments(db: Session = Depends(get_db)):
    return db.query(Assessment).all()