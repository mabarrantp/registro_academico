from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from models.subject import Subject

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("/")
def list_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()