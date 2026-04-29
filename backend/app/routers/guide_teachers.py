from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from security import get_current_user, require_roles

from models.guide_teacher_assignment import GuideTeacherAssignment
from models.teacher import Teacher
from models.grade import Grade
from models.section import Section


router = APIRouter(
    prefix="/guide-teachers",
    tags=["Guide Teacher"]
)

# =====================================================
# ASIGNAR MAESTRO GUÍA
# =====================================================
@router.post("")
def assign_guide_teacher(
    teacher_id: int,
    grade_id: int,
    section_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Asigna un maestro guía a una sección en un año académico.
    """
    require_roles("ADMIN", "COORDINATION")(user)

    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    if section.grade_id != grade.id:
        raise HTTPException(
            status_code=400,
            detail="La sección no pertenece al grado indicado"
        )

    existing = db.query(GuideTeacherAssignment).filter(
        GuideTeacherAssignment.grade_id == grade_id,
        GuideTeacherAssignment.section_id == section_id,
        GuideTeacherAssignment.academic_year == academic_year
    ).first()

    if existing:
        existing.teacher_id = teacher_id
    else:
        db.add(GuideTeacherAssignment(
            teacher_id=teacher_id,
            grade_id=grade_id,
            section_id=section_id,
            academic_year=academic_year
        ))

    db.commit()

    return {
        "teacher_id": teacher_id,
        "grade": grade.name,
        "section": section.code,
        "academic_year": academic_year
    }


# =====================================================
# VER MAESTRO GUÍA DE UNA SECCIÓN
# =====================================================
@router.get("")
def get_guide_teacher(
    grade_id: int,
    section_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_roles("ADMIN", "COORDINATION", "TEACHER")(user)

    guide = db.query(GuideTeacherAssignment).filter(
        GuideTeacherAssignment.grade_id == grade_id,
        GuideTeacherAssignment.section_id == section_id,
        GuideTeacherAssignment.academic_year == academic_year
    ).first()

    if not guide:
        return None

    return {
        "teacher_id": guide.teacher_id,
        "grade_id": guide.grade_id,
        "section_id": guide.section_id,
        "academic_year": guide.academic_year
    }