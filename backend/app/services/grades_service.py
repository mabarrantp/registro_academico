from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.grade import Grade
from app.models.student import Student
from app.models.subject import Subject
from app.models.quarter import Quarter
from app.models.section import Section


# =====================================================
# Helper: conversión cuantitativa → cualitativa
# (misma regla institucional)
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
# Servicio: obtener notas (Grades)
# =====================================================

def get_grades(
    *,
    db: Session,
    student_id: Optional[int] = None,
    section_id: Optional[int] = None,
    quarter_id: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Obtiene notas según filtros.
    - Puede filtrar por estudiante
    - Puede filtrar por sección
    - Puede filtrar por quarter

    ❗ No contiene lógica HTTP
    ❗ No valida roles
    """

    query = (
        db.query(
            Grade,
            Student.first_name,
            Student.last_name,
            Subject.name.label("subject_name"),
            Quarter.code.label("quarter"),
            Section.label.label("grade_label"),
        )
        .join(Student, Student.id == Grade.student_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Quarter, Quarter.id == Grade.quarter_id)
        .join(Section, Section.id == Grade.section_id)
    )

    if student_id:
        query = query.filter(Grade.student_id == student_id)

    if section_id:
        query = query.filter(Grade.section_id == section_id)

    if quarter_id:
        query = query.filter(Grade.quarter_id == quarter_id)

    results = query.all()

    response: List[Dict[str, Any]] = []

    for grade, first_name, last_name, subject_name, quarter, grade_label in results:
        response.append({
            "student": f"{first_name} {last_name}",
            "grade": grade_label,
            "subject": subject_name,
            "quarter": quarter,
            "quantitative": grade.final_grade,
            "qualitative": to_qualitative(grade.final_grade),
        })

    return response


# =====================================================
# Servicio: promedio final por estudiante
# =====================================================

def get_final_average_by_student(
    *,
    db: Session,
    student_id: int,
) -> Dict[str, Any]:
    """
    Calcula el promedio final del estudiante
    en todas las materias y quarters.
    """

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError("Estudiante no encontrado")

    avg = (
        db.query(func.avg(Grade.final_grade))
        .filter(Grade.student_id == student_id)
        .scalar()
    )

    avg = round(avg, 2) if avg is not None else None

    return {
        "student": f"{student.first_name} {student.last_name}",
        "final_average": avg,
        "final_qualitative": to_qualitative(avg),
    }

