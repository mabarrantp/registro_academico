from sqlalchemy.orm import Session

from app.models.teacher import Teacher
from app.models.subject import Subject
from app.models.section import Section
from app.models.teacher_assignment import TeacherAssignment


ACADEMIC_YEAR = 2025


def seed_teacher_assignments(db: Session):
    assignments = [
        # (Apellido del docente, Nombre de la materia, Código de sección)
        ("Lara", "Bible", "A"),
        ("Herrera", "Biology", "A"),
        ("Vilchez", "Chemistry", "B"),
        ("Alonso", "Physics", "A"),
        ("Palacio", "Spanish", "B"),
    ]

    created = 0
    skipped = 0

    for teacher_last, subject_name, section_code in assignments:
        teacher = db.query(Teacher).filter(Teacher.last_name == teacher_last).first()
        subject = db.query(Subject).filter(Subject.name == subject_name).first()
        section = db.query(Section).filter(Section.code == section_code).first()

        if not teacher or not subject or not section:
            skipped += 1
            continue

        exists = (
            db.query(TeacherAssignment)
            .filter(
                TeacherAssignment.teacher_id == teacher.id,
                TeacherAssignment.subject_id == subject.id,
                TeacherAssignment.section_id == section.id,
                TeacherAssignment.academic_year == ACADEMIC_YEAR,
            )
            .first()
        )

        if exists:
            skipped += 1
        else:
            db.add(
                TeacherAssignment(
                    teacher_id=teacher.id,
                    subject_id=subject.id,
                    section_id=section.id,
                    academic_year=ACADEMIC_YEAR,
                )
            )
            created += 1

    db.commit()
    print(f"✅ Teacher assignments | created={created} skipped={skipped}")
