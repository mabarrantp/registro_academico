from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.security import get_current_user
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.subject import Subject
from app.models.assessment import Assessment

router = APIRouter(
    prefix="/dashboard/admin",
    tags=["Dashboard - Admin"],
)


@router.get("/summary")
def admin_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Solo administración")

    return {
        "students": db.query(func.count(Student.id)).scalar(),
        "teachers": db.query(func.count(Teacher.id)).scalar(),
        "subjects": db.query(func.count(Subject.id)).scalar(),
        "assessments": db.query(func.count(Assessment.id)).scalar(),
    }
