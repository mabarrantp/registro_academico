from app.database import SessionLocal
from app.models.teacher import Teacher
from app.models.subject import Subject
from app.models.teacher_specialty import TeacherSpecialty

db = SessionLocal()

def link(teacher_name, subject_names):
    teacher = (
        db.query(Teacher)
        .filter(Teacher.first_name == teacher_name)
        .first()
    )
    for name in subject_names:
        subject = db.query(Subject).filter(Subject.name == name).first()
        if teacher and subject:
            exists = (
                db.query(TeacherSpecialty)
                .filter(
                    TeacherSpecialty.teacher_id == teacher.id,
                    TeacherSpecialty.subject_id == subject.id
                )
                .first()
            )
            if not exists:
                db.add(
                    TeacherSpecialty(
                        teacher_id=teacher.id,
                        subject_id=subject.id
                    )
                )

# === ESPECIALIDADES ===
link("Rosa", ["Math", "Physics"])
link("Edwin", ["Biology", "Chemistry", "Science"])
link("María", ["Math", "Lengua y Literatura"])
link("Marcos", ["Computer"])
link("Fatima", ["Spanish"])
link("Ana", ["Language Arts", "ESL"])

db.commit()
db.close()

print("✅ TeacherSpecialty cargadas")