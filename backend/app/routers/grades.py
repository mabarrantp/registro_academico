from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.security import get_current_user
from app.services.grades_service import (
    get_grades,
    get_final_average_by_student,
)
from app.schemas.grades import (
    GradesResponseSchema,
    FinalAverageSchema,
)


# =====================================================
# Router
# =====================================================

router = APIRouter(
    prefix="/grades",
    tags=["Grades"],
)


# =====================================================
# GET /grades
# 👉 Listado de notas (con filtros)
# =====================================================

@router.get(
    "",
    response_model=GradesResponseSchema,
    summary="Obtener notas",
    description="Devuelve el listado de notas según los filtros aplicados.",
)
def list_grades(
    student_id: Optional[int] = Query(None, description="ID del estudiante"),
    section_id: Optional[int] = Query(None, description="ID de la sección"),
    quarter_id: Optional[int] = Query(None, description="ID del quarter"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 🔒 Control de acceso
    if user.role not in ("TEACHER", "ADMIN", "COORDINATION"):
        raise HTTPException(status_code=403, detail="No autorizado")

    grades = get_grades(
        db=db,
        student_id=student_id,
        section_id=section_id,
        quarter_id=quarter_id,
    )

    return {"grades": grades}


# =====================================================
# GET /grades/final-average
# 👉 Promedio final del estudiante
# =====================================================

@router.get(
    "/final-average",
    response_model=FinalAverageSchema,
    summary="Promedio final del estudiante",
    description="Calcula el promedio final del estudiante en todas las materias.",
)
def get_final_average(
    student_id: int = Query(..., description="ID del estudiante"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 🔒 Control de acceso
    if user.role not in ("TEACHER", "ADMIN", "COORDINATION"):
        raise HTTPException(status_code=403, detail="No autorizado")

    try:
        return get_final_average_by_student(
            db=db,
            student_id=student_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))