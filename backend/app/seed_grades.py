from sqlalchemy.orm import Session

from app.models.grade import Grade


def seed_grades(db: Session):
    grades_data = [
        {"code": "1st", "order": 1, "level": "PRIMARY", "label": "1st Grade"},
        {"code": "2nd", "order": 2, "level": "PRIMARY", "label": "2nd Grade"},
        {"code": "3rd", "order": 3, "level": "PRIMARY", "label": "3rd Grade"},
        {"code": "4th", "order": 4, "level": "PRIMARY", "label": "4th Grade"},
        {"code": "5th", "order": 5, "level": "PRIMARY", "label": "5th Grade"},
        {"code": "6th", "order": 6, "level": "PRIMARY", "label": "6th Grade"},
        {"code": "7th", "order": 7, "level": "SECONDARY", "label": "7th Grade"},
        {"code": "8th", "order": 8, "level": "SECONDARY", "label": "8th Grade"},
        {"code": "9th", "order": 9, "level": "SECONDARY", "label": "9th Grade"},
        {"code": "10th", "order": 10, "level": "SECONDARY", "label": "10th Grade"},
        {"code": "11th", "order": 11, "level": "SECONDARY", "label": "11th Grade"},
    ]

    for g in grades_data:
        exists = db.query(Grade).filter(Grade.code == g["code"]).first()
        if not exists:
            db.add(Grade(**g, active=True))

    db.commit()
    print("✅ Grades sembrados")
