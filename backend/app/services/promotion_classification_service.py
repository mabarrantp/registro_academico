from app.models.final_grade import FinalGrade
from app.models.promotion_result import PromotionResult


def classify_students(db, academic_year_id: int):
    results = []

    grades = (
        db.query(FinalGrade)
        .filter(FinalGrade.academic_year_id == academic_year_id)
        .all()
    )

    for grade in grades:
        if grade.average >= 60:
            status = "APROBADO"
        elif grade.average >= 50:
            status = "REPARACION"
        else:
            status = "REPETIDOR"

        result = PromotionResult(
            student_id=grade.student_id,
            academic_year_id=academic_year_id,
            result=status
        )
        db.add(result)
        results.append(result)

    db.commit()
    return results

