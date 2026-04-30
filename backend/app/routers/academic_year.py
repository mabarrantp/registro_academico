from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.academic_year import (
    AcademicYearCreate,
    AcademicYearResponse
)
from app.services import academic_year_service

router = APIRouter(
    prefix="/academic-years",
    tags=["Academic Years"]
)


@router.get("", response_model=list[AcademicYearResponse])
def list_academic_years(db: Session = Depends(get_db)):
    return academic_year_service.get_all_academic_years(db)


@router.post("", response_model=AcademicYearResponse)
def create_academic_year(
    data: AcademicYearCreate,
    db: Session = Depends(get_db)
):
    return academic_year_service.create_academic_year(db, data)


@router.post("/{year_id}/open", response_model=AcademicYearResponse)
def open_academic_year(
    year_id: int,
    db: Session = Depends(get_db)
):
    return academic_year_service.open_academic_year(db, year_id)


@router.post("/{year_id}/close", response_model=AcademicYearResponse)
def close_academic_year(
    year_id: int,
    db: Session = Depends(get_db)
):
    return academic_year_service.close_academic_year(db, year_id)

