from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.report_card_service import get_report_card

router = APIRouter(prefix="/report-card", tags=["Report Card"])


@router.get("/")
def report_card(
    student_id: int,
    subject_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
):
    data = get_report_card(db, student_id, subject_id, academic_year)
    if not data:
        raise HTTPException(404, "Report card not found")
    return data
