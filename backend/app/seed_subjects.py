from app.database import SessionLocal
from app.models.subject import Subject

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

for s in subjects:
    if not db.query(Subject).filter(Subject.name == s.name).first():
        db.add(s)

db.commit()
db.close()

print("✅ Subjects cargados")
