from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict

from app.database import get_db
from app.security import get_current_user
from app.models.quarter_weight import QuarterWeight
from app.models.teacher_assignment import TeacherAssignment
from app.models.quarter import Quarter
from app.schemas.quarter_weight import QuarterWeightsPayload


router = APIRouter(
    prefix="/quarter-weights",
    tags=["Quarter Weights"],
)


# -------------------------------------------------
# ✅ Helper: validar suma de ponderaciones
# -------------------------------------------------
def validate_weights(weights: Dict[str, int]):
    total = sum(weights.values())
    if total != 100:
        raise HTTPException(
            status_code=400,
            detail=f"La suma de ponderaciones debe ser 100 (actual: {total})",
        )


# -------------------------------------------------
# ✅ Helper: validar que el quarter esté OPEN
# -------------------------------------------------
def validate_quarter_open(db: Session, quarter_id: int):
    quarter = db.query(Quarter).filter(Quarter.id == quarter_id).first()
    if not quarter:
        raise HTTPException(status_code=404, detail="Quarter no encontrado")

    if quarter.status == "CLOSED":
        raise HTTPException(
            status_code=400,
            detail=f"El quarter {quarter.code} está cerrado. No se pueden modificar ponderaciones.",
        )

    return quarter


# -------------------------------------------------
# ✅ GET: ver ponderaciones del quarter
# (LECTURA SIEMPRE PERMITIDA)
# -------------------------------------------------
@router.get("")
def get_quarter_weights(
    assignment_id: int = Query(...),
    quarter_id: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Solo docentes")

    assignment = (
        db.query(TeacherAssignment)
        .filter(
            TeacherAssignment.id == assignment_id,
            TeacherAssignment.teacher_id == user.teacher_id,
        )
        .first()
    )
    if not assignment:
        raise HTTPException(status_code=403, detail="Asignación no válida")

    weight = (
        db.query(QuarterWeight)
        .filter(
            QuarterWeight.quarter_id == quarter_id,
            QuarterWeight.subject_id == assignment.subject_id,
            QuarterWeight.section_id == assignment.section_id,
        )
        .first()
    )

    if not weight:
        return {
            "exists": False,
            "weights": {},
        }

    return {
        "exists": True,
        "id": weight.id,
        "weights": weight.weights,
    }


# -------------------------------------------------
# ✅ POST: crear ponderaciones
# (BLOQUEADO SI QUARTER = CLOSED)
# -------------------------------------------------
@router.post("")
def create_quarter_weights(
    payload: QuarterWeightsPayload,
    assignment_id: int = Query(...),
    quarter_id: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Solo docentes")

    # 🔒 Validar quarter abierto
    validate_quarter_open(db, quarter_id)

    weights = payload.weights
    validate_weights(weights)

    assignment = (
        db.query(TeacherAssignment)
        .filter(
            TeacherAssignment.id == assignment_id,
            TeacherAssignment.teacher_id == user.teacher_id,
        )
        .first()
    )
    if not assignment:
        raise HTTPException(status_code=403, detail="Asignación no válida")

    existing = (
        db.query(QuarterWeight)
        .filter(
            QuarterWeight.quarter_id == quarter_id,
            QuarterWeight.subject_id == assignment.subject_id,
            QuarterWeight.section_id == assignment.section_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Las ponderaciones ya existen para este quarter",
        )

    weight = QuarterWeight(
        quarter_id=quarter_id,
        subject_id=assignment.subject_id,
        section_id=assignment.section_id,
        weights=weights,
    )

    db.add(weight)
    db.commit()
    db.refresh(weight)

    return {
        "id": weight.id,
        "weights": weight.weights,
    }


# -------------------------------------------------
# ✅ PUT: editar ponderaciones
# (BLOQUEADO SI QUARTER = CLOSED)
# -------------------------------------------------
@router.put("/{weight_id}")
def update_quarter_weights(
    weight_id: int,
    payload: QuarterWeightsPayload,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Solo docentes")

    weight = db.query(QuarterWeight).filter(QuarterWeight.id == weight_id).first()
    if not weight:
        raise HTTPException(status_code=404, detail="No encontrado")

    # 🔒 Validar quarter abierto
    validate_quarter_open(db, weight.quarter_id)

    assignment = (
        db.query(TeacherAssignment)
        .filter(
            TeacherAssignment.subject_id == weight.subject_id,
            TeacherAssignment.section_id == weight.section_id,
            TeacherAssignment.teacher_id == user.teacher_id,
        )
        .first()
    )
    if not assignment:
        raise HTTPException(status_code=403, detail="No autorizado")

    weights = payload.weights
    validate_weights(weights)

    weight.weights = weights
    db.commit()

    return {
        "id": weight.id,
        "weights": weight.weights,
    }
