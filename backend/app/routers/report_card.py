from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import pdfkit

from app.database import get_db
from app.security import get_current_user
from app.services.report_card_service import build_report_card
from app.schemas.report_card import ReportCardResponseSchema


# =====================================================
# Router
# =====================================================

router = APIRouter(
    prefix="/report-card",
    tags=["Report Card"],
)

templates = Jinja2Templates(directory="app/templates")


# =====================================================
# GET /report-card
# 👉 JSON oficial del boletín (con schema)
# =====================================================

@router.get(
    "",
    response_model=ReportCardResponseSchema,
    summary="Obtener boletín académico",
    description="Devuelve el boletín académico oficial del estudiante para un año académico.",
)
def get_report_card(
    student_id: int = Query(..., description="ID del estudiante"),
    academic_year: int = Query(..., description="Año académico"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 🔒 Control de acceso
    if user.role not in ("TEACHER", "ADMIN", "COORDINATION"):
        raise HTTPException(status_code=403, detail="No autorizado")

    try:
        return build_report_card(
            db=db,
            student_id=student_id,
            academic_year=academic_year,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =====================================================
# GET /report-card/pdf
# 👉 PDF oficial del boletín
# =====================================================

@router.get(
    "/pdf",
    summary="Descargar boletín académico en PDF",
    description="Genera el boletín académico oficial del estudiante en formato PDF.",
)
def get_report_card_pdf(
    student_id: int = Query(..., description="ID del estudiante"),
    academic_year: int = Query(..., description="Año académico"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 🔒 Control de acceso
    if user.role not in ("TEACHER", "ADMIN", "COORDINATION"):
        raise HTTPException(status_code=403, detail="No autorizado")

    try:
        data = build_report_card(
            db=db,
            student_id=student_id,
            academic_year=academic_year,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    html = templates.get_template("report_card.html").render(data)
    pdf = pdfkit.from_string(html, False)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "inline; filename=report_card.pdf"
        },
    )
