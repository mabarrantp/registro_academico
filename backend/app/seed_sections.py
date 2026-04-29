from sqlalchemy.orm import Session
from app.models.grade import Grade
from app.models.section import Section


def seed_sections(db: Session):
    grades = db.query(Grade).all()

    for grade in grades:
        for code in ["A", "B"]:
            exists = (
                db.query(Section)
                .filter(
                    Section.grade_id == grade.id,
                    Section.code == code,
                )
                .first()
            )
            if not exists:
                db.add(
                    Section(
                        grade_id=grade.id,
                        code=code,
                        active=True,
                    )
                )

    db.commit()
    print("✅ Sections sembradas")
