from database import SessionLocal
from models.subject import Subject


def run():
    db = SessionLocal()

    subjects = [
        Subject(name="Bible", category="RELIGION"),
        Subject(name="Biology", category="SCIENCE"),
        Subject(name="Chemistry", category="SCIENCE"),
        Subject(name="Physics", category="SCIENCE"),
        Subject(name="Science", category="SCIENCE"),
        Subject(name="Health", category="SCIENCE"),
        Subject(name="History", category="HUMANITIES"),
        Subject(name="Geographic", category="HUMANITIES"),
        Subject(name="Estudios Sociales", category="HUMANITIES"),
        Subject(name="Economic", category="HUMANITIES"),
        Subject(name="Philosophy", category="HUMANITIES"),
        Subject(name="Civic", category="HUMANITIES"),
        Subject(name="Spanish", category="LANGUAGE"),
        Subject(name="Lengua y Literatura", category="LANGUAGE"),
        Subject(name="Language Arts", category="LANGUAGE"),
        Subject(name="ESL", category="LANGUAGE"),
        Subject(name="Math", category="CORE"),
        Subject(name="Computer", category="COMPLEMENTARY"),
        Subject(name="Music", category="COMPLEMENTARY"),
        Subject(name="P.E", category="COMPLEMENTARY"),
        Subject(name="Creciendo en Valores", category="VALUES"),
        Subject(name="Dignidad y Derechos de la Mujer", category="VALUES"),
        Subject(name="AEP", category="VALUES"),
    ]

    created = 0
    skipped = 0

    for s in subjects:
        if db.query(Subject).filter(Subject.name == s.name).first():
            skipped += 1
        else:
            db.add(s)
            created += 1

    db.commit()
    db.close()

    print(f"✅ Subjects cargados | created={created} skipped={skipped}")


if __name__ == "__main__":
    run()
