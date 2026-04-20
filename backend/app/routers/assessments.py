from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.deps import require_roles
from app.utils.quarter_guard import ensure_quarter_open
from app.services.audit_service import log_event

from app.models.assessment import Assessment
from app.models.student import Student
from app.models.subject import Subject
from app.models.teacher import Teacher
from app.models.grade import Grade
from app.models.quarter import Quarter
from app.models.assessment_category import AssessmentCategory

router = APIRouter(prefix="/assessments", tags=["Assessments"])

ALLOWED_ROLES = ("TEACHER", "ADMIN", "COORDINATION")


def to_dict(a: Assessment):
    return {
        "id": a.id,
        "student_id": a.student_id,
        "subject_id": a.subject_id,
        "teacher_id": a.teacher_id,
        "grade_id": a.grade_id,
        "quarter_id": a.quarter_id,
        "category_id": a.category_id,
        "score": a.score,
        "on_time": a.on_time,
        "comments": a.comments,
        "status": a.status,
    }


@router.post("/", dependencies=[Depends(require_roles(*ALLOWED_ROLES))])
def create_assessment(
    student_id: int,
    subject_id: int,
    teacher_id: int,
    grade_id: int,
    quarter_id: int,
    category_id: int,
    score: float,
    on_time: bool = True,
    comments: str | None = None,
    db: Session = Depends(get_db),
):
    ensure_quarter_open(db, quarter_id)

    if not db.query(Student).filter(Student.id == student_id).first():
        raise HTTPException(status_code=404, detail="Student not found")
    if not db.query(Subject).filter(Subject.id == subject_id).first():
        raise HTTPException(status_code=404, detail="Subject not found")
    if not db.query(Teacher).filter(Teacher.id == teacher_id).first():
        raise HTTPException(status_code=404, detail="Teacher not found")
    if not db.query(Grade).filter(Grade.id == grade_id).first():
        raise HTTPException(status_code=404, detail="Grade not found")
    if not db.query(Quarter).filter(Quarter.id == quarter_id).first():
        raise HTTPException(status_code=404, detail="Quarter not found")
    if not db.query(AssessmentCategory).filter(AssessmentCategory.id == category_id).first():
        raise HTTPException(status_code=404, detail="Assessment category not found")

    a = Assessment(
        student_id=student_id,
        subject_id=subject_id,
        teacher_id=teacher_id,
        grade_id=grade_id,
        quarter_id=quarter_id,
        category_id=category_id,
        score=score,
        on_time=on_time,
        comments=comments,
        status="ACTIVE",
    )

    try:
        db.add(a)
        db.commit()
        db.refresh(a)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database constraint error: {str(e.orig)}")

    try:
        log_event(
            db=db,
            entity_type="Assessment",
            entity_id=a.id,
            action="CREATE",
            performed_by="teacher",
            new_value=str(score),
        )
    except Exception:
        pass

    # ✅ retorno explícito -> nunca será {}
    return to_dict(a)


@router.post("/{assessment_id}/exclude", dependencies=[Depends(require_roles(*ALLOWED_ROLES))])
def exclude_assessment(assessment_id: int, db: Session = Depends(get_db)):
    a = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found")

    ensure_quarter_open(db, a.quarter_id)

    old = a.status
    a.status = "EXCLUDED"
    db.commit()
    db.refresh(a)

    try:
        log_event(db=db, entity_type="Assessment", entity_id=a.id,
                  action="EXCLUDE", performed_by="teacher",
                  old_value=old, new_value="EXCLUDED")
    except Exception:
        pass

    return to_dict(a)


@router.post("/{assessment_id}/activate", dependencies=[Depends(require_roles(*ALLOWED_ROLES))])
def activate_assessment(assessment_id: int, db: Session = Depends(get_db)):
    a = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found")

    ensure_quarter_open(db, a.quarter_id)

    old = a.status
    a.status = "ACTIVE"
    db.commit()
    db.refresh(a)

    try:
        log_event(db=db, entity_type="Assessment", entity_id=a.id,
                  action="ACTIVATE", performed_by="teacher",
                  old_value=old, new_value="ACTIVE")
    except Exception:
        pass

    return to_dict(a)


@router.get("/", dependencies=[Depends(require_roles(*ALLOWED_ROLES))])
def list_assessments(db: Session = Depends(get_db)):
    rows = db.query(Assessment).all()
    return [to_dict(a) for a in rows]
