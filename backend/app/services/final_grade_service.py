from sqlalchemy.orm import Session
from app.models.quarter_grade import QuarterGrade
from app.models.final_grade import FinalGrade
from app.models.quarter import Quarter

def calculate_final_grade(
    db: Session,
    student_id: int,
    subject_id: int,
    academic_year: int,
):
    quarters = (
        db.query(Quarter)
        .filter(Quarter.academic_year == academic_year)
        .all()
    )

    if not quarters:
        return None

    quarter_ids = [q.id for q in quarters]

    grades = (
        db.query(QuarterGrade)
        .filter(
            QuarterGrade.student_id == student_id,
            QuarterGrade.subject_id == subject_id,
            QuarterGrade.quarter_id.in_(quarter_ids),
        )
        .all()
    )

    if not grades:
        return None

    avg = sum(g.final_score for g in grades) / len(grades)

    record = (
        db.query(FinalGrade)
        .filter(
            FinalGrade.student_id == student_id,
            FinalGrade.subject_id == subject_id,
            FinalGrade.academic_year == academic_year,
        )
        .first()
    )

    if record:
        record.final_score = avg
    else:
        record = FinalGrade(
            student_id=student_id,
            subject_id=subject_id,
            academic_year=academic_year,
            final_score=avg,
        )
        db.add(record)

    db.commit()
    return record
