from database import SessionLocal
from models.teacher import Teacher
from models.subject import Subject
from models.teacher_specialty import TeacherSpecialty


def run():
    db = SessionLocal()

    def link(teacher_name, subject_names):
        teacher = (
            db.query(Teacher)
            .filter(Teacher.first_name == teacher_name)
            .first()
        )

        if not teacher:
            return

        for name in subject_names:
            subject = db.query(Subject).filter(Subject.name == name).first()
            if not subject:
                continue

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


if __name__ == "__main__":
    run()
