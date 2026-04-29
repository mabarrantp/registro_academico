from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict

from app.database import get_db
from security import get_current_user, require_roles

from models.student import Student
from models.enrollment import Enrollment
from models.quarter_grade import QuarterGrade
from models.subject import Subject
from models.quarter import Quarter


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# =====================================================
# 1️⃣ BOLETÍN / REPORT CARD DEL ESTUDIANTE
# =====================================================
@router.get("/report-card/{student_id}")
def report_card(
    student_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Boletín del estudiante para un año académico.
    """
    require_roles("ADMIN", "COORDINATION", "TEACHER")(user)

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    grades = (
        db.query(QuarterGrade)
        .join(Quarter)
        .filter(
            QuarterGrade.student_id == student_id,
            QuarterGrade.academic_year == academic_year
        )
        .all()
    )

    if not grades:
        return {
            "student": {
                "id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "academic_year": academic_year
            },
            "subjects": {}
        }

    by_subject = defaultdict(dict)

    for g in grades:
        by_subject[g.subject_id][g.quarter_id] = g.final_grade

    return {
        "student": {
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "academic_year": academic_year
        },
        "subjects": by_subject
    }


# =====================================================
# 2️⃣ PROMEDIO FINAL DEL AÑO (FG)
# =====================================================
@router.get("/final-grade/{student_id}")
def final_grade(
    student_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Promedio final del año académico.
    """
    require_roles("ADMIN", "COORDINATION", "TEACHER")(user)

    grades = (
        db.query(QuarterGrade)
        .filter(
            QuarterGrade.student_id == student_id,
            QuarterGrade.academic_year == academic_year
        )
        .all()
    )

    if not grades:
        return {
            "student_id": student_id,
            "academic_year": academic_year,
            "final_grade": None
        }

    avg = round(
        sum(g.final_grade for g in grades) / len(grades),
        2
    )

    return {
        "student_id": student_id,
        "academic_year": academic_year,
        "final_grade": avg
    }


# =====================================================
# 3️⃣ REPORTE POR GRADO (ADMIN / COORDINATION)
# =====================================================
@router.get("/by-grade")
def report_by_grade(
    grade_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_roles("ADMIN", "COORDINATION")(user)

    enrollments = (
        db.query(Enrollment)
        .filter(
            Enrollment.grade_id == grade_id,
            Enrollment.academic_year == academic_year
        )
        .all()
    )

    result = []

    for e in enrollments:
        grades = (
            db.query(QuarterGrade)
            .filter(
                QuarterGrade.student_id == e.student_id,
                QuarterGrade.academic_year == academic_year
            )
            .all()
        )

        if not grades:
            continue

        avg = round(
            sum(g.final_grade for g in grades) / len(grades),
            2
        )

        result.append({
            "student_id": e.student_id,
            "final_grade": avg
        })

    return result


# =====================================================
# 4️⃣ REPORTE POR SECCIÓN (ADMIN / COORDINATION / TEACHER)
# =====================================================
@router.get("/by-section")
def report_by_section(
    section_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_roles("ADMIN", "COORDINATION", "TEACHER")(user)

    enrollments = (
        db.query(Enrollment)
        .filter(
            Enrollment.section_id == section_id,
            Enrollment.academic_year == academic_year
        )
        .all()
    )

    result = []

    for e in enrollments:
        grades = (
            db.query(QuarterGrade)
            .filter(
                QuarterGrade.student_id == e.student_id,
                QuarterGrade.academic_year == academic_year
            )
            .all()
        )

        if not grades:
            continue

        avg = round(
            sum(g.final_grade for g in grades) / len(grades),
            2
        )

        result.append({
            "student_id": e.student_id,
            "final_grade": avg
        })

    return result