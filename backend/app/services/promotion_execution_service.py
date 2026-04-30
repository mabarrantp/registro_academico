from app.models.promotion_result import PromotionResult
from app.models.enrollment import Enrollment


def execute_promotion(db, academic_year_id: int):
    promotions = (
        db.query(PromotionResult)
        .filter(PromotionResult.academic_year_id == academic_year_id)
        .all()
    )

    for p in promotions:
        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id == p.student_id,
                Enrollment.academic_year_id == academic_year_id
            )
            .first()
        )
        if not enrollment:
            continue

        if p.result == "APROBADO":
            enrollment.promoted = True
        else:
            enrollment.promoted = False

    db.commit()

