from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.services.academic_year_service import get_active_academic_year


def import_enrollments_from_excel(db: Session, rows: list[dict]):
    active_year = get_active_academic_year(db)
    if not active_year:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Enrollment import requires an active academic year"
        )

    created = 0
    errors = []

    for index, row in enumerate(rows, start=1):
        exists = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id == row["student_id"],
                Enrollment.section_id == row["section_id"],
                Enrollment.academic_year_id == active_year.id
            )
            .first()
        )

        if exists:
            errors.append({"row": index, "error": "Duplicate enrollment"})
            continue

        enrollment = Enrollment(
            student_id=row["student_id"],
            section_id=row["section_id"],
            academic_year_id=active_year.id
        )
        db.add(enrollment)
        created += 1

    db.commit()

    return {
        "created": created,
        "errors": errors
    }

