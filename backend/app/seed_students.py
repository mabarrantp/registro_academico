from app.database import SessionLocal
from app.models.student import Student

db = SessionLocal()

students = [
    Student(first_name="Juan", last_name="Pérez"),
    Student(first_name="María", last_name="Gómez"),
    Student(first_name="Carlos", last_name="López"),
]

for s in students:
    exists = (
        db.query(Student)
        .filter(Student.first_name == s.first_name, Student.last_name == s.last_name)
        .first()
    )
    if not exists:
        db.add(s)

db.commit()
db.close()

print("✅ Students cargados")
