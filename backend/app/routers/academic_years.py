from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.security import get_current_user
from app.models.quarter import Quarter


router = APIRouter(
    prefix="/academic-years",
    tags=["Academic Years"],
)


# -------------------------------------------------
# ✅ POST /academic-years/open
# Abre un nuevo año académico y crea Q1–Q4
# -------------------------------------------------
@router.post("/open")
def open_academic_year(
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 🔒 Solo administración o coordinación
    if user.role not in ("ADMIN", "COORDINATION"):
        raise HTTPException(
            status_code=403,
            detail="Solo administración o coordinación puede abrir un nuevo año académico",
        )

    # ✅ Verificar si ya existe ese año
    existing = (
        db.query(Quarter)
        .filter(Quarter.academic_year == academic_year)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"El año académico {academic_year} ya existe",
        )

    # ✅ Crear Q1–Q4
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    created = []

    for code in quarters:
        db.add(
            Quarter(
                code=code,
                academic_year=academic_year,
                status="OPEN",
            )
        )
        created.append(code)

    db.commit()

    return {
        "academic_year": academic_year,
        "quarters_created": created,
        "status": "OPEN",
        "message": f"Año académico {academic_year} abierto correctamente",
    }


