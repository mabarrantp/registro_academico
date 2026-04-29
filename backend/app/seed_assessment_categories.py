from app.database import SessionLocal
from models.assessment_category import AssessmentCategory


def run():
    db = SessionLocal()

    categories = [
        AssessmentCategory(code="QUIZ"),
        AssessmentCategory(code="HOMEWORK"),
        AssessmentCategory(code="CLASSWORK"),
        AssessmentCategory(code="PROJECT"),
        AssessmentCategory(code="TEST"),
    ]

    created = 0
    skipped = 0

    for c in categories:
        exists = (
            db.query(AssessmentCategory)
            .filter(AssessmentCategory.code == c.code)
            .first()
        )

        if exists:
            skipped += 1
        else:
            db.add(c)
            created += 1

    db.commit()
    db.close()

    print(f"✅ AssessmentCategories cargadas | created={created} skipped={skipped}")


if __name__ == "__main__":
    run()