from app.database import SessionLocal
from app.models.assessment_category import AssessmentCategory

db = SessionLocal()

categories = [
    AssessmentCategory(code="QUIZ"),
    AssessmentCategory(code="HOMEWORK"),
    AssessmentCategory(code="CLASSWORK"),
    AssessmentCategory(code="PROJECT"),
    AssessmentCategory(code="TEST"),
]

for c in categories:
    exists = (
        db.query(AssessmentCategory)
        .filter(AssessmentCategory.code == c.code)
        .first()
    )
    if not exists:
        db.add(c)

db.commit()
db.close()

print("✅ AssessmentCategories cargadas")
