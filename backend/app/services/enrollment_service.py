from fastapi import HTTPException, status
from app.services.academic_year_service import get_active_academic_year


def create_enrollment(db, data):
    active_year = get_active_academic_year(db)

    if not active_year:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Enrollment not allowed without an active academic year"
        )

    enrollment = Enrollment(
        student_id=data.student_id,
        section_id=data.section_id,
        academic_year_id=active_year.id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

