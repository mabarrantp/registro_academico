from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.grade import Grade
from app.models.quarter import Quarter
from app.models.subject import Subject
from app.models.section import Section


# =====================================================
# Helper: cuantitativo → cualitativo
# =====================================================

def to_qualitative(score: Optional[float]) -> str:
    if score is None:
        return ""
    if score >= 90:
        return "AA"   # Advanced Learning
    if score >= 76:
        return "AS"   # Satisfactory Learning
    if score >= 60:
        return "AF"   # Elementary Learning
    return "AI"       # Improvement Needed


# =====================================================
# Servicio principal: Report Card
# =====================================================

def build_report_card(
    *,
    db: Session,
    student_id: int,
    academic_year: int,
) -> Dict[str, Any]:
    """
    Construye el Report Card académico de un estudiante
    para un año académico específico.

    ❗ No contiene lógica HTTP
    ❗ No valida roles
    ❗ No lanza HTTPExceptions
    """

    # -------------------------------------------------
    # Estudiante
    # -------------------------------------------------
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError("Estudiante no encontrado")

    # -------------------------------------------------
    # Quarters del año académico
    # -------------------------------------------------
    quarters = (
        db.query(Quarter)
        .filter(Quarter.academic_year == academic_year)
        .order_by(Quarter.id)
        .all()
    )

    if not quarters:
        raise ValueError("No existen quarters para este año académico")

    quarter_map = {q.id: q.code for q in quarters}

    # -------------------------------------------------
    # Notas
    # -------------------------------------------------
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

    # -------------------------------------------------
    # Construcción del reporte
    # -------------------------------------------------
    report: Dict[str, Dict[str, Any]] = {}

    for grade, subject_name, grade_label in grades:
        if subject_name not in report:
            report[subject_name] = {
                "subject": subject_name,
                "grade": grade_label,
                "quarters": {},
                "final_sum": 0,
                "final_count": 0,
            }

        quarter_code = quarter_map.get(grade.quarter_id)

        report[subject_name]["quarters"][quarter_code] = {
            "quantitative": grade.final_grade,
            "qualitative": to_qualitative(grade.final_grade),
        }

        if grade.final_grade is not None:
            report[subject_name]["final_sum"] += grade.final_grade
            report[subject_name]["final_count"] += 1

    # -------------------------------------------------
    # Respuesta final
    # -------------------------------------------------
    response: List[Dict[str, Any]] = []

    for item in report.values():
        average = (
            round(item["final_sum"] / item["final_count"], 2)
            if item["final_count"] > 0
            else None
        )

        response.append({
            "subject": item["subject"],
            "grade": item["grade"],
            "quarters": item["quarters"],
            "final_average": average,
            "final_qualitative": to_qualitative(average),
        })

    return {
        "student": f"{student.first_name} {student.last_name}",
        "academic_year": academic_year,
        "report_card": response,
    }
