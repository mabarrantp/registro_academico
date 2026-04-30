from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.student import Student
from app.services.academic_year_service import get_active_academic_year
from app.services.student_import_validator import validate_student_import_row


def import_students_from_excel(db: Session, rows: list[dict]):
    active_year = get_active_academic_year(db)
    if not active_year:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot import students without an active academic year"
        )

    created = 0
    errors = []

    for index, row in enumerate(rows, start=1):
        error = validate_student_import_row(row)
        if error:
            errors.append({"row": index, "error": error})
            continue

        student = Student(
            external_id=row["id_externo"],
            first_name=row["nombres"],
            last_name=row["apellidos"],
            birth_date=row["fecha_nacimiento"],
            document=row["documento_identidad"],
            is_active=True
        )

        db.add(student)
        created += 1

    db.commit()

    return {
        "created": created,
        "errors": errors
    }

def deactivate_student(db: Session, student_id: int):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.is_active = False
    db.commit()
    db.refresh(student)
    return student
