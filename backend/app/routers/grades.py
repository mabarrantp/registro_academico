from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.grade import Grade

router = APIRouter(prefix="/grades", tags=["Grades"])


@router.post("/")
def create_grade(name: str, level: str, db: Session = Depends(get_db)):
    exists = db.query(Grade).filter(Grade.name == name).first()
    if exists:
        raise HTTPException(400, "Grade already exists")
    grade = Grade(name=name, level=level)
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade


@router.get("/")
def list_grades(db: Session = Depends(get_db)):
    return db.query(Grade).all()