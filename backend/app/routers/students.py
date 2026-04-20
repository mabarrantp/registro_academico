from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/")
def create_student(first_name: str, last_name: str, db: Session = Depends(get_db)):
    student = Student(first_name=first_name, last_name=last_name)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/")
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()
