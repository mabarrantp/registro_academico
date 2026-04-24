from sqlalchemy.orm import Session
from models.quarter import Quarter
from models.quarter_grade import QuarterGrade
from models.final_grade import FinalGrade

def get_report_card(db: Session, student_id: int, subject_id: int, academic_year: int):
    quarters = (
        db.query(Quarter)
        .filter(Quarter.academic_year == academic_year)
        .all()
    )

    quarter_map = {q.code: None for q in quarters}

    grades = (
        db.query(QuarterGrade)
        .filter(
            QuarterGrade.student_id == student_id,
            QuarterGrade.subject_id == subject_id,
            QuarterGrade.quarter_id.in_([q.id for q in quarters]),
        )
        .all()
    )

    for g in grades:
        q = next(q for q in quarters if q.id == g.quarter_id)
        quarter_map[q.code] = round(g.final_score, 2)

    final = (
        db.query(FinalGrade)
        .filter(
            FinalGrade.student_id == student_id,
            FinalGrade.subject_id == subject_id,
            FinalGrade.academic_year == academic_year,
        )
        .first()
    )

    return {
        "student_id": student_id,
        "subject_id": subject_id,
        "academic_year": academic_year,
        "quarters": quarter_map,
        "final_grade": round(final.final_score, 2) if final else None,
    }