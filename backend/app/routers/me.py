from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user
from app.models.teacher_assignment import TeacherAssignment
from app.models.subject import Subject
from app.models.section import Section
from app.models.grade import Grade


router = APIRouter(
    prefix="/me",
    tags=["Me"],
)


@router.get("/teacher-assignments")
def my_teacher_assignments(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Solo para docentes")

    assignments = (
        db.query(
            TeacherAssignment.id,
            Subject.name,
            Grade.label,
            Section.code,
            TeacherAssignment.academic_year,
        )
        .join(Subject, TeacherAssignment.subject_id == Subject.id)
        .join(Section, TeacherAssignment.section_id == Section.id)
        .join(Grade, Section.grade_id == Grade.id)
        .filter(TeacherAssignment.teacher_id == user.teacher_id)
        .all()
    )

    return [
        {
            "assignment_id": aid,
            "subject": subject,
            "grade": grade,
            "section": section,
            "academic_year": year,
        }
        for aid, subject, grade, section, year in assignments
    ]
