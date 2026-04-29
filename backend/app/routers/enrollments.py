from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.grade import Grade
from app.models.section import Section

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("")
def create_enrollment(
    student_code: str,
    grade_id: int,
    section_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
):
    student = (
        db.query(Student)
        .filter(Student.student_code == student_code)
        .first()
    )

    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    exists = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student.id,
            Enrollment.academic_year == academic_year,
        )
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="El estudiante ya está matriculado en este año",
        )

    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    section = db.query(Section).filter(Section.id == section_id).first()

    if not grade or not section:
        raise HTTPException(status_code=400, detail="Grado o sección inválidos")

    enrollment = Enrollment(
        student_id=student.id,
        grade_id=grade_id,
        section_id=section_id,
        academic_year=academic_year,
    )

    student.current_grade_id = grade_id

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return {
        "id": enrollment.id,
        "student_code": student.student_code,
        "academic_year": academic_year,
    }
