from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import defaultdict

from app.database import get_db
from security import get_current_user, require_roles

from models.assessment import Assessment
from models.enrollment import Enrollment
from models.student import Student
from models.subject import Subject


router = APIRouter(
    prefix="/risk",
    tags=["Academic Risk"]
)

# Límites pedagógicos
RISK_LIMIT = 65
HIGH_RISK_LIMIT = 60


@router.get("")
def academic_risk(
    grade_id: int,
    section_id: int,
    quarter_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Devuelve estudiantes en riesgo académico
    mientras el quarter está ABIERTO.
    """
    require_roles("ADMIN", "COORDINATION", "TEACHER")(user)

    enrollments = db.query(Enrollment).filter(
        Enrollment.grade_id == grade_id,
        Enrollment.section_id == section_id,
        Enrollment.academic_year == academic_year
    ).all()

    results = []

    for e in enrollments:
        assessments = db.query(Assessment).filter(
            Assessment.student_id == e.student_id,
            Assessment.quarter_id == quarter_id,
            Assessment.academic_year == academic_year
        ).all()

        if not assessments:
            continue

        by_subject = defaultdict(list)
        for a in assessments:
            by_subject[a.subject_id].append(a.score)

        student = db.query(Student).filter(
            Student.id == e.student_id
        ).first()

        for subject_id, scores in by_subject.items():
            avg = sum(scores) / len(scores)

            if avg < RISK_LIMIT:
                subject = db.query(Subject).filter(
                    Subject.id == subject_id
                ).first()

                level = "HIGH" if avg < HIGH_RISK_LIMIT else "MEDIUM"

                results.append({
                    "student_id": student.id,
                    "student": f"{student.first_name} {student.last_name}",
                    "subject_id": subject_id,
                    "subject": subject.name if subject else f"Subject {subject_id}",
                    "average": round(avg, 2),
                    "risk_level": level
                })

    return results