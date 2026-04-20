from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.final_grade_service import calculate_final_grade

router = APIRouter(prefix="/final-grades", tags=["Final Grades"])


@router.post("/calculate")
def calculate(
    student_id: int,
    subject_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
):
    result = calculate_final_grade(
        db,
        student_id,
        subject_id,
        academic_year,
    )
    if not result:
        raise HTTPException(404, "QuarterGrades not found")
    return result
