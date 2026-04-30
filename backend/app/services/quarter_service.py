from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.quarter import Quarter, QuarterStatus
from app.services.academic_year_service import get_active_academic_year


def open_quarter(db: Session, quarter_id: int):
    # ✅ Validación institucional
    active_year = get_active_academic_year(db)
    if not active_year:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot open quarter without an active academic year"
        )

    quarter = db.query(Quarter).get(quarter_id)
    if not quarter:
        raise HTTPException(status_code=404, detail="Quarter not found")

    if quarter.status == QuarterStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot open a closed quarter"
        )

    # Cerrar cualquier otro quarter activo
    active_quarter = (
        db.query(Quarter)
        .filter(Quarter.status == QuarterStatus.ACTIVE)
        .first()
    )
    if active_quarter and active_quarter.id != quarter.id:
        active_quarter.status = QuarterStatus.CLOSED

    quarter.status = QuarterStatus.ACTIVE
    db.commit()
    db.refresh(quarter)

    return quarter


def close_quarter(db: Session, quarter_id: int):
    # ✅ Validación institucional (también aplica aquí)
    active_year = get_active_academic_year(db)
    if not active_year:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot close quarter without an active academic year"
        )

    quarter = db.query(Quarter).get(quarter_id)
    if not quarter:
        raise HTTPException(status_code=404, detail="Quarter not found")

    if quarter.status == QuarterStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Quarter already closed"
        )

    quarter.status = QuarterStatus.CLOSED
    db.commit()
    db.refresh(quarter)

    return quarter
