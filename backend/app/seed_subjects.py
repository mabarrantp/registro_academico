from sqlalchemy.orm import Session
from app.models.subject import Subject


def seed_subjects(db: Session):
    subjects = [
        ("Bible", "RELIGION"),
        ("Biology", "SCIENCE"),
        ("Chemistry", "SCIENCE"),
        ("Physics", "SCIENCE"),
        ("Science", "SCIENCE"),
        ("Health", "SCIENCE"),
        ("History", "HUMANITIES"),
        ("Geographic", "HUMANITIES"),
        ("Estudios Sociales", "HUMANITIES"),
        ("Economic", "HUMANITIES"),
        ("Philosophy", "HUMANITIES"),
        ("Civic", "HUMANITIES"),
        ("Spanish", "LANGUAGE"),
        ("Lengua y Literatura", "LANGUAGE"),
        ("Language Arts", "LANGUAGE"),
        ("ESL", "LANGUAGE"),
        ("Math", "CORE"),
        ("Computer", "COMPLEMENTARY"),
        ("Music", "COMPLEMENTARY"),
        ("P.E", "COMPLEMENTARY"),
        ("Creciendo en Valores", "VALUES"),
        ("Dignidad y Derechos de la Mujer", "VALUES"),
        ("AEP", "VALUES"),
    ]

    created = 0
    skipped = 0

    for name, category in subjects:
        exists = db.query(Subject).filter(Subject.name == name).first()
        if exists:
            skipped += 1
        else:
            db.add(Subject(name=name, category=category))
            created += 1

    db.commit()
    print(f"✅ Subjects sembradas | created={created} skipped={skipped}")