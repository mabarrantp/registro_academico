from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from security import get_current_user, require_roles

from models.academic_record import AcademicRecord
from models.academic_record_signature import AcademicRecordSignature


router = APIRouter(
    prefix="/academic-record-signatures",
    tags=["Academic Record Signatures"]
)

# Roles que DEBEN firmar para que el acta sea válida
REQUIRED_ROLES = {"GUIDE_TEACHER", "COORDINATION"}

# =====================================================
# FIRMAR ACTA ACADÉMICA
# =====================================================
@router.post("/sign")
def sign_academic_record(
    academic_record_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Firma digital de un acta académica.
    """
    role = user.role  # viene del token JWT

    if role not in REQUIRED_ROLES and role != "DIRECTOR":
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para firmar actas"
        )

    record = db.query(AcademicRecord).filter(
        AcademicRecord.id == academic_record_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Acta no encontrada")

    existing = db.query(AcademicRecordSignature).filter(
        AcademicRecordSignature.academic_record_id == academic_record_id,
        AcademicRecordSignature.role == role
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Este rol ya firmó esta acta"
        )

    signature = AcademicRecordSignature(
        academic_record_id=academic_record_id,
        user_id=user.id,
        role=role
    )

    db.add(signature)
    db.commit()
    db.refresh(signature)

    return {
        "academic_record_id": academic_record_id,
        "signed_by": role,
        "signed_at": signature.signed_at
    }


# =====================================================
# VER ESTADO DE FIRMAS DEL ACTA
# ✅ ESTE ES EL MÉTODO QUE PREGUNTABAS
# =====================================================
@router.get("/status")
def academic_record_signature_status(
    academic_record_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Devuelve el estado de firmas del acta académica.
    """
    signatures = db.query(AcademicRecordSignature).filter(
        AcademicRecordSignature.academic_record_id == academic_record_id
    ).all()

    signed_roles = {s.role for s in signatures}

    return {
        "academic_record_id": academic_record_id,
        "signed_roles": list(signed_roles),
        "is_fully_signed": REQUIRED_ROLES.issubset(signed_roles)
    }