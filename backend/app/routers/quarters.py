from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.quarter import Quarter
from app.deps import require_roles

router = APIRouter(prefix="/quarters", tags=["Quarters"])

# ✅ Roles que pueden ver la lista
READ_ROLES = ("TEACHER", "COORDINATION", "ADMIN")

# ✅ Roles que pueden abrir/cerrar (NO TEACHER)
MANAGE_ROLES = ("COORDINATION", "ADMIN")


@router.get("/", dependencies=[Depends(require_roles(*READ_ROLES))])
def list_quarters(db: Session = Depends(get_db)):
    return db.query(Quarter).all()


@router.post("/{quarter_id}/close", dependencies=[Depends(require_roles(*MANAGE_ROLES))])
def close_quarter(quarter_id: int, db: Session = Depends(get_db)):
    q = db.query(Quarter).filter(Quarter.id == quarter_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quarter not found")

    q.status = "CLOSED"
    db.commit()
    db.refresh(q)
    return q


@router.post("/{quarter_id}/open", dependencies=[Depends(require_roles(*MANAGE_ROLES))])
def open_quarter(quarter_id: int, db: Session = Depends(get_db)):
    q = db.query(Quarter).filter(Quarter.id == quarter_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quarter not found")

    q.status = "OPEN"
    db.commit()
    db.refresh(q)
    return q
