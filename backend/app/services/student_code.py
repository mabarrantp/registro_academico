from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.student import Student
from app.models.grade import Grade


def generate_student_code(
    db: Session,
    entry_year: int,
    entry_grade_id: int
) -> str:
    """
    Genera código institucional del estudiante:
    YYYY-NN-XXXX
    """

    grade = db.query(Grade).filter(Grade.id == entry_grade_id).first()
    if not grade:
        raise ValueError("Grado de ingreso no existe")

    if grade.level == "PRIMARY":
        level_code = "01"
    elif grade.level == "SECONDARY":
        level_code = "02"
    else:
        raise ValueError("Nivel educativo no soportado")

    prefix = f"{entry_year}-{level_code}"

    last_code = (
        db.query(func.max(Student.student_code))
        .filter(Student.student_code.like(f"{prefix}-%"))
        .scalar()
    )

    if last_code:
        last_seq = int(last_code.split("-")[-1])
        next_seq = last_seq + 1
    else:
        next_seq = 1

    return f"{prefix}-{str(next_seq).zfill(4)}"
