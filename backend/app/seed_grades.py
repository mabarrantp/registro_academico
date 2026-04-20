from app.database import SessionLocal
from app.models.grade import Grade

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

for g in grades:
    exists = db.query(Grade).filter(Grade.name == g.name).first()
    if not exists:
        db.add(g)

db.commit()
db.close()

print("✅ Grades cargados")