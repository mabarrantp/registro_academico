from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.enrollment import Enrollment

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("/")
def enroll_student(student_id: int, grade_id: int, academic_year: int, db: Session = Depends(get_db)):
    exists = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student_id,
            Enrollment.grade_id == grade_id,
            Enrollment.academic_year == academic_year
        )
        .first()
    )
    if exists:
        raise HTTPException(400, "Student already enrolled")

    enrollment = Enrollment(
        student_id=student_id,
        grade_id=grade_id,
        academic_year=academic_year
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/")
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()
