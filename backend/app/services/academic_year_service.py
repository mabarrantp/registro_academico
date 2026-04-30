from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.academic_year import AcademicYear, AcademicYearStatus
from app.models.quarter import Quarter


def get_active_academic_year(db: Session):
    return (
        db.query(AcademicYear)
        .filter(AcademicYear.status == AcademicYearStatus.ACTIVE)
        .first()
    )


def list_academic_years(db: Session):
    return db.query(AcademicYear).order_by(AcademicYear.start_date.desc()).all()


def create_academic_year(db: Session, data):
    year = AcademicYear(
        name=data.name,
        start_date=data.start_date,
        end_date=data.end_date,
        status=AcademicYearStatus.CREATED
    )
    db.add(year)
    db.commit()
    db.refresh(year)
    return year


def open_academic_year(db: Session, year_id: int):
    year = db.query(AcademicYear).get(year_id)
    if not year:
        raise HTTPException(status_code=404, detail="Academic year not found")

    if year.status == AcademicYearStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot open a closed academic year"
        )

    active = get_active_academic_year(db)
    if active and active.id != year.id:
        active.status = AcademicYearStatus.CREATED

    year.status = AcademicYearStatus.ACTIVE
    year.opened_at = datetime.utcnow()

    db.commit()
    db.refresh(year)
    return year


def close_academic_year(db: Session, year_id: int):
    year = db.query(AcademicYear).get(year_id)
    if not year:
        raise HTTPException(status_code=404, detail="Academic year not found")

    open_quarter = (
        db.query(Quarter)
        .filter(Quarter.status == "OPEN")
        .first()
    )
    if open_quarter:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot close academic year with an open quarter"
        )

    year.status = AcademicYearStatus.CLOSED
    year.closed_at = datetime.utcnow()

    db.commit()
    db.refresh(year)
    return year


# ✅ FUNCIÓN ESPERADA POR ETAPA C
def close_active_academic_year(db: Session):
    year = get_active_academic_year(db)
    if not year:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active academic year"
        )

    return close_academic_year(db, year.id)
