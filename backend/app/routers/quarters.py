from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user
from app.models.quarter import Quarter
from app.models.quarter_weight import QuarterWeight
from app.models.teacher_assignment import TeacherAssignment


router = APIRouter(
    prefix="/quarters",
    tags=["Quarters"],
)


#---------------------------------------------------
# ✅ GET /quarters
# Lista todos los quarters (para frontend, NO adivinar IDs)
# -------------------------------------------------
@router.get("")
def list_quarters(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    quarters = db.query(Quarter).order_by(Quarter.id).all()

    return [
        {
            "id": q.id,
            "code": q.code,
            "academic_year": q.academic_year,
            "status": q.status,
        }
        for q in quarters
    ]


# -------------------------------------------------
# ✅ GET /quarters/{quarter_id}/status
# Estado del quarter (UX-friendly)
# -------------------------------------------------
@router.get("/{quarter_id}/status")
def get_quarter_status(
    quarter_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    quarter = db.query(Quarter).filter(Quarter.id == quarter_id).first()
    if not quarter:
        raise HTTPException(status_code=404, detail="Quarter no encontrado")

    return {
        "quarter_id": quarter.id,
        "code": quarter.code,
        "status": quarter.status,
    }


# -------------------------------------------------
# ✅ POST /quarters/{quarter_id}/close
# Cerrar quarter (regla académica)
# -------------------------------------------------
@router.post("/{quarter_id}/close")
def close_quarter(
    quarter_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    quarter = db.query(Quarter).filter(Quarter.id == quarter_id).first()
    if not quarter:
        raise HTTPException(status_code=404, detail="Quarter no encontrado")

    if quarter.status == "CLOSED":
        return {
            "quarter_id": quarter.id,
            "status": quarter.status,
            "message": "El quarter ya está cerrado",
        }

    # ✅ Regla mínima: deben existir ponderaciones
    has_weights = (
        db.query(QuarterWeight)
        .filter(QuarterWeight.quarter_id == quarter_id)
        .first()
    )

    if not has_weights:
        raise HTTPException(
            status_code=400,
            detail="No se puede cerrar el quarter sin ponderaciones definidas",
        )

    quarter.status = "CLOSED"
    db.commit()

    return {
        "quarter_id": quarter.id,
        "status": quarter.status,
        "message": f"Quarter {quarter.code} cerrado correctamente",
    }


# -------------------------------------------------
# ✅ POST /quarters/{quarter_id}/open
# Reabrir quarter (solo coordinación / admin)
# -------------------------------------------------
@router.post("/{quarter_id}/open")
def open_quarter(
    quarter_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role not in ("ADMIN", "COORDINATION"):
        raise HTTPException(
            status_code=403,
            detail="Solo administración o coordinación puede reabrir el quarter",
        )

    quarter = db.query(Quarter).filter(Quarter.id == quarter_id).first()
    if not quarter:
        raise HTTPException(status_code=404, detail="Quarter no encontrado")

    quarter.status = "OPEN"
    db.commit()

    return {
        "quarter_id": quarter.id,
        "status": quarter.status,
        "message": f"Quarter {quarter.code} reabierto correctamente",
    }

