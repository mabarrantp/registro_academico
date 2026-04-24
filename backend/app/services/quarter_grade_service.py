from sqlalchemy.orm import Session
from models.assessment import Assessment
from models.assessment_category import AssessmentCategory
from models.grade_policy import GradePolicy
from models.quarter_grade import QuarterGrade
from services.audit_service import log_event


def calculate_quarter_grade(
    db: Session,
    student_id: int,
    subject_id: int,
    grade_id: int,
    quarter_id: int,
    teacher_id: int,
    academic_year: int,
):
    policy = (
        db.query(GradePolicy)
        .filter(
            GradePolicy.teacher_id == teacher_id,
            GradePolicy.subject_id == subject_id,
            GradePolicy.grade_id == grade_id,
            GradePolicy.quarter_id == quarter_id,
            GradePolicy.academic_year == academic_year,
        )
        .first()
    )

    if not policy:
        return None

    def avg(category_code: str) -> float:
        category = (
            db.query(AssessmentCategory)
            .filter(AssessmentCategory.code == category_code)
            .first()
        )
        if not category:
            return 0.0

        rows = (
            db.query(Assessment)
            .filter(
                Assessment.student_id == student_id,
                Assessment.subject_id == subject_id,
                Assessment.grade_id == grade_id,
                Assessment.quarter_id == quarter_id,
                Assessment.category_id == category.id,
                Assessment.status == "ACTIVE",  # ✅ SOLO ACTIVAS
            )
            .all()
        )

        if not rows:
            return 0.0

        return sum(r.score for r in rows) / len(rows)

    quiz_avg = avg("QUIZ")
    homework_avg = avg("HOMEWORK")
    classwork_avg = avg("CLASSWORK")
    project_avg = avg("PROJECT")
    test_avg = avg("TEST")

    final_score = (
        quiz_avg * policy.quiz_weight
        + homework_avg * policy.homework_weight
        + classwork_avg * policy.classwork_weight
        + project_avg * policy.project_weight
        + test_avg * policy.test_weight
    )

    record = (
        db.query(QuarterGrade)
        .filter(
            QuarterGrade.student_id == student_id,
            QuarterGrade.subject_id == subject_id,
            QuarterGrade.quarter_id == quarter_id,
        )
        .first()
    )

    if record:
        old_value = str(record.final_score)
        record.final_score = final_score
        action = "RECALCULATE"
    else:
        record = QuarterGrade(
            student_id=student_id,
            subject_id=subject_id,
            quarter_id=quarter_id,
            final_score=final_score,
        )
        db.add(record)
        db.flush()
        old_value = None
        action = "CALCULATE"

    db.commit()

    log_event(
        db=db,
        entity_type="QuarterGrade",
        entity_id=record.id,
        action=action,
        performed_by="system",
        old_value=old_value,
        new_value=str(round(final_score, 2)),
    )

    return record
