from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from security import get_current_user, require_roles

from models.academic_record import AcademicRecord
from models.guide_teacher_assignment import GuideTeacherAssignment
from models.promotion_result import PromotionResult
from models.enrollment import Enrollment
from models.student import Student


router = APIRouter(prefix="/academic-records", tags=["Academic Records"])


@router.post("/generate")
def generate_academic_record(
    grade_id: int,
    section_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_roles("ADMIN", "COORDINATION")(user)

    guide = db.query(GuideTeacherAssignment).filter(
        GuideTeacherAssignment.grade_id == grade_id,
        GuideTeacherAssignment.section_id == section_id,
        GuideTeacherAssignment.academic_year == academic_year
    ).first()

    if not guide:
        raise HTTPException(status_code=404, detail="Maestro guía no asignado")

    record = AcademicRecord(
        grade_id=grade_id,
        section_id=section_id,
        academic_year=academic_year,
        guide_teacher_id=guide.teacher_id
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "academic_record_id": record.id,
        "grade_id": grade_id,
        "section_id": section_id,
        "academic_year": academic_year
    }
