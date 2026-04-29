from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.security import get_current_user
from app.models.assessment import Assessment
from app.models.teacher_assignment import TeacherAssignment
from app.models.quarter import Quarter
from app.models.student import Student


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)


# -------------------------------------------------
# ✅ Helper: validar quarter OPEN
# -------------------------------------------------
def validate_quarter_open(db: Session, quarter_id: int):
    quarter = db.query(Quarter).filter(Quarter.id == quarter_id).first()
    if not quarter:
        raise HTTPException(status_code=404, detail="Quarter no encontrado")

    if quarter.status == "CLOSED":
        raise HTTPException(
            status_code=400,
            detail=f"El quarter {quarter.code} está cerrado. No se pueden modificar evaluaciones.",
        )


# -------------------------------------------------
# ✅ POST: crear evaluación por EVENTO (batch)
# -------------------------------------------------
@router.post("/event")
def create_assessment_event(
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Solo docentes")

    assignment_id = payload.get("assignment_id")
    quarter_id = payload.get("quarter_id")
    assessment_type = payload.get("assessment_type")
    topic = payload.get("topic")
    assigned_date_str = payload.get("assigned_date")
    grades = payload.get("grades", [])

    if not all([assignment_id, quarter_id, assessment_type, topic, assigned_date_str]):
        raise HTTPException(status_code=400, detail="Datos incompletos")

    try:
        assigned_date = date.fromisoformat(assigned_date_str)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="assigned_date debe tener formato YYYY-MM-DD",
        )

    validate_quarter_open(db, quarter_id)

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

    created = 0

    for g in grades:
        student = db.query(Student).filter(Student.id == g["student_id"]).first()
        if not student:
            continue

        db.add(
            Assessment(
                teacher_assignment_id=assignment_id,
                student_id=student.id,
                quarter=quarter_id,
                assessment_type=assessment_type,
                topic=topic,
                assigned_date=assigned_date,
                score=g["score"],
            )
        )
        created += 1

    db.commit()

    return {
        "message": "Evaluación creada correctamente",
        "assessment_type": assessment_type,
        "topic": topic,
        "students_evaluated": created,
    }


# -------------------------------------------------
# ✅ GET: listar evaluaciones (WORKFLOW)
# -------------------------------------------------
@router.get("/events")
def list_assessment_events(
    assignment_id: int,
    quarter_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Solo docentes")

    events = (
        db.query(
            Assessment.assessment_type,
            Assessment.topic,
            Assessment.assigned_date,
        )
        .filter(
            Assessment.teacher_assignment_id == assignment_id,
            Assessment.quarter == quarter_id,
        )
        .group_by(
            Assessment.assessment_type,
            Assessment.topic,
            Assessment.assigned_date,
        )
        .order_by(Assessment.assigned_date.desc())
        .all()
    )

    return [
        {
            "assessment_type": e.assessment_type,
            "topic": e.topic,
            "assigned_date": e.assigned_date,
        }
        for e in events
    ]


# -------------------------------------------------
# ✅ GET: detalle de evaluación por EVENTO
# -------------------------------------------------
@router.get("/event/detail")
def get_assessment_event_detail(
    assignment_id: int,
    quarter_id: int,
    assessment_type: str,
    topic: str,
    assigned_date: str,  # ✅ STRING (Pydantic v2 safe)
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Solo docentes")

    try:
        assigned_date_obj = date.fromisoformat(assigned_date)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="assigned_date debe tener formato YYYY-MM-DD",
        )

    records = (
        db.query(Assessment, Student)
        .join(Student, Student.id == Assessment.student_id)
        .filter(
            Assessment.teacher_assignment_id == assignment_id,
            Assessment.quarter == quarter_id,
            Assessment.assessment_type == assessment_type,
            Assessment.topic == topic,
            Assessment.assigned_date == assigned_date_obj,
        )
        .order_by(Student.last_name)
        .all()
    )

    if not records:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    return {
        "assessment_type": assessment_type,
        "topic": topic,
        "assigned_date": assigned_date,
        "grades": [
            {
                "student_id": s.id,
                "student_name": f"{s.first_name} {s.last_name}",
                "score": a.score,
            }
            for a, s in records
        ],
    }


# -------------------------------------------------
# ✅ PUT: editar notas del EVENTO (batch)
# -------------------------------------------------
@router.put("/event")
def update_assessment_event(
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Solo docentes")

    assignment_id = payload.get("assignment_id")
    quarter_id = payload.get("quarter_id")
    assessment_type = payload.get("assessment_type")
    topic = payload.get("topic")
    assigned_date_str = payload.get("assigned_date")
    grades = payload.get("grades", [])

    if not all([assignment_id, quarter_id, assessment_type, topic, assigned_date_str]):
        raise HTTPException(status_code=400, detail="Datos incompletos")

    try:
        assigned_date = date.fromisoformat(assigned_date_str)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="assigned_date debe tener formato YYYY-MM-DD",
        )

    validate_quarter_open(db, quarter_id)

    records = (
        db.query(Assessment)
        .filter(
            Assessment.teacher_assignment_id == assignment_id,
            Assessment.quarter == quarter_id,
            Assessment.assessment_type == assessment_type,
            Assessment.topic == topic,
            Assessment.assigned_date == assigned_date,
        )
        .all()
    )

    if not records:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    updated = 0

    for r in records:
        for g in grades:
            if r.student_id == g["student_id"]:
                r.score = g["score"]
                updated += 1

    db.commit()

    return {
        "message": "Evaluación actualizada correctamente",
        "students_updated": updated,
    }


# -------------------------------------------------
# ✅ DELETE: eliminar EVENTO completo
# -------------------------------------------------
@router.delete("/event")
def delete_assessment_event(
    assignment_id: int,
    quarter_id: int,
    assessment_type: str,
    topic: str,
    assigned_date: str,  # ✅ STRING
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Solo docentes")

    try:
        assigned_date_obj = date.fromisoformat(assigned_date)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="assigned_date debe tener formato YYYY-MM-DD",
        )

    validate_quarter_open(db, quarter_id)

    deleted = (
        db.query(Assessment)
        .filter(
            Assessment.teacher_assignment_id == assignment_id,
            Assessment.quarter == quarter_id,
            Assessment.assessment_type == assessment_type,
            Assessment.topic == topic,
            Assessment.assigned_date == assigned_date_obj,
        )
        .delete()
    )

    db.commit()

    return {
        "message": "Evaluación eliminada correctamente",
        "records_deleted": deleted,
    }