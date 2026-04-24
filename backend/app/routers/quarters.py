from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.quarter import Quarter
from security import get_current_user, require_roles

router = APIRouter(
    prefix="/quarters",
    tags=["Quarters"]
)


@router.get("/")
def list_quarters(db: Session = Depends(get_db)):
    return db.query(Quarter).all()


@router.post("/{quarter_id}/close")
def close_quarter(
    quarter_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    # 🔒 SOLO ADMIN Y COORDINATION
    require_roles("ADMIN", "COORDINATION")(user)

    quarter = db.query(Quarter).filter(
        Quarter.id == quarter_id
    ).first()

    if not quarter:
        raise HTTPException(
            status_code=404,
            detail="Quarter not found"
        )

    quarter.status = "CLOSED"
    db.commit()

    return {"status": "Quarter closed"}


@router.post("/{quarter_id}/open")
def open_quarter(
    quarter_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    # 🔒 SOLO ADMIN Y COORDINATION
    require_roles("ADMIN", "COORDINATION")(user)

    quarter = db.query(Quarter).filter(
        Quarter.id == quarter_id
    ).first()

    if not quarter:
        raise HTTPException(
            status_code=404,
            detail="Quarter not found"
        )

    quarter.status = "OPEN"
    db.commit()

    return {"status": "Quarter opened"}
