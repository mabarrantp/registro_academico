from database import SessionLocal
from models.grade import Grade


def run():
    db = SessionLocal()

    grades = [
        # PRIMARIA
        Grade(name="1°", level="PRIMARIA"),
        Grade(name="2°", level="PRIMARIA"),
        Grade(name="3°", level="PRIMARIA"),
        Grade(name="4°", level="PRIMARIA"),
        Grade(name="5°", level="PRIMARIA"),
        Grade(name="6°", level="PRIMARIA"),
        # SECUNDARIA
        Grade(name="7°", level="SECUNDARIA"),
        Grade(name="8°", level="SECUNDARIA"),
        Grade(name="9°", level="SECUNDARIA"),
        Grade(name="10°", level="SECUNDARIA"),
        Grade(name="11°", level="SECUNDARIA"),
    ]

    created = 0
    skipped = 0

    for g in grades:
        if db.query(Grade).filter(Grade.name == g.name).first():
            skipped += 1
        else:
            db.add(g)
            created += 1

    db.commit()
    db.close()

    print(f"✅ Grades cargados | created={created} skipped={skipped}")


if __name__ == "__main__":
    run()