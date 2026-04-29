from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
import pdfkit
import os

from app.database import get_db
from app.security import get_current_user
from app.models.student import Student
from app.models.grade import Grade
from app.models.quarter import Quarter
from app.models.subject import Subject
from app.models.section import Section


# =====================================================
# Router
# =====================================================

router = APIRouter(
    prefix="/report-card",
    tags=["Report Card"],
)

templates = Jinja2Templates(directory="app/templates")


# =====================================================
# Helper: cuantitativo → cualitativo
# =====================================================

def to_qualitative(score: Optional[float]) -> str:
    if score is None:
        return ""
    if score >= 90:
        return "AA"
    if score >= 76:
        return "AS"
    if score >= 60:
        return "AF"
    return "AI"


# =====================================================
# GET /report-card
# =====================================================

@router.get("")
def get_report_card(
    student_id: int = Query(...),
    academic_year: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role not in ("TEACHER", "ADMIN", "COORDINATION"):
        raise HTTPException(status_code=403, detail="No autorizado")

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    quarters = (
        db.query(Quarter)
        .filter(Quarter.academic_year == academic_year)
        .order_by(Quarter.id)
        .all()
    )

    quarter_map = {q.id: q.code for q in quarters}

    grades = (
        db.query(
            Grade,
            Subject.name.label("subject_name"),
            Section.label.label("grade_label"),
        )
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Section, Section.id == Grade.section_id)
        .filter(
            Grade.student_id == student_id,
            Grade.quarter_id.in_(quarter_map.keys()),
        )
        .all()
    )

    report = {}

    for g, subject_name, grade_label in grades:
        if subject_name not in report:
            report[subject_name] = {
                "subject": subject_name,
                "grade": grade_label,
                "quarters": {},
                "sum": 0,
                "count": 0,
            }

        qc = quarter_map[g.quarter_id]
        report[subject_name]["quarters"][qc] = {
            "quantitative": g.final_grade,
            "qualitative": to_qualitative(g.final_grade),
        }

        if g.final_grade is not None:
            report[subject_name]["sum"] += g.final_grade
            report[subject_name]["count"] += 1

    response = []
    for item in report.values():
        avg = round(item["sum"] / item["count"], 2) if item["count"] else None
        response.append({
            "subject": item["subject"],
            "grade": item["grade"],
            "quarters": item["quarters"],
            "final_average": avg,
            "final_qualitative": to_qualitative(avg),
        })

    return {
        "student": f"{student.first_name} {student.last_name}",
        "academic_year": academic_year,
        "report_card": response,
    }


# =====================================================
# GET /report-card/pdf  (WKHTMLTOPDF)
# =====================================================

@router.get("/pdf")
def get_report_card_pdf(
    student_id: int = Query(...),
    academic_year: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    data = get_report_card(student_id, academic_year, db, user)

    html = templates.get_template("report_card.html").render(data)

    pdf = pdfkit.from_string(html, False)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "inline; filename=report_card.pdf"
        },
    )
