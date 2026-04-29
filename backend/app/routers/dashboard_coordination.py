from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.security import get_current_user
from app.models.assessment import Assessment
from app.models.teacher_assignment import TeacherAssignment
from app.models.section import Section
from app.models.grade import Grade
from app.models.teacher import Teacher
from app.models.student import Student

router = APIRouter(
    prefix="/dashboard/coordination",
    tags=["Dashboard - Coordination"],
)


def require_coordination(user):
    if user.role not in ("ADMIN", "COORDINATION"):
        raise HTTPException(status_code=403, detail="Solo coordinación o administración")


# ✅ Resumen general
@router.get("/summary")
def coordination_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_coordination(user)

    total_students = db.query(func.count(Student.id)).scalar()
    total_teachers = db.query(func.count(Teacher.id)).scalar()
    avg_score = db.query(func.avg(Assessment.score)).scalar()

    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "average_score": round(avg_score, 2) if avg_score else None,
    }


# ✅ Promedios por grado
@router.get("/average-by-grade")
def average_by_grade(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_coordination(user)

    results = (
        db.query(
            Grade.label,
            func.avg(Assessment.score).label("average"),
        )
        .join(Section, Section.grade_id == Grade.id)
        .join(TeacherAssignment, TeacherAssignment.section_id == Section.id)
        .join(Assessment, Assessment.teacher_assignment_id == TeacherAssignment.id)
        .group_by(Grade.label)
        .all()
    )

    return [
        {"grade": grade, "average": round(avg, 2)}
        for grade, avg in results
    ]


# ✅ Docentes con estudiantes en riesgo
@router.get("/teachers-at-risk")
def teachers_with_risk_students(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_coordination(user)

    results = (
        db.query(
            Teacher.id,
            Teacher.first_name,
            Teacher.last_name,
            func.avg(Assessment.score).label("average"),
        )
        .join(TeacherAssignment, TeacherAssignment.teacher_id == Teacher.id)
        .join(Assessment, Assessment.teacher_assignment_id == TeacherAssignment.id)
        .group_by(Teacher.id)
        .having(func.avg(Assessment.score) < 60)
        .all()
    )

    return [
        {
            "teacher_id": tid,
            "teacher": f"{first} {last}",
            "average": round(avg, 2),
        }
        for tid, first, last, avg in results
    ]
