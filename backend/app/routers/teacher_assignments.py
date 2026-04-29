from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user
from app.models.teacher_assignment import TeacherAssignment

router = APIRouter(
    prefix="/teacher-assignments",
    tags=["Teacher Assignments"],
)


@router.get("")
def list_teacher_assignments(
    academic_year: int | None = Query(None, description="Año académico"),
    teacher_id: int | None = Query(None, description="ID del docente"),
    section_id: int | None = Query(None, description="ID de la sección"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    query = db.query(TeacherAssignment)

    # 🔹 Filtros opcionales
    if academic_year is not None:
        query = query.filter(
            TeacherAssignment.academic_year == academic_year
        )

    if teacher_id is not None:
        query = query.filter(
            TeacherAssignment.teacher_id == teacher_id
        )

    if section_id is not None:
        query = query.filter(
            TeacherAssignment.section_id == section_id
        )

    # 🔒 Restricción por rol
    # Docente solo ve sus asignaciones
    if user.role == "TEACHER":
        query = query.filter(
            TeacherAssignment.teacher_id == user.teacher_id
        )

    return query.all()
