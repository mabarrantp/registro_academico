from database import SessionLocal
from models.teacher_role import TeacherRole


def run():
    db = SessionLocal()

    roles = [
        ("GUIDE_TEACHER", "Maestro guía"),
        ("SUBJECT_TEACHER", "Profesor de asignatura"),
        ("COMPLEMENTARY_TEACHER", "Profesor complementario"),
    ]

    created = 0
    skipped = 0

    for code, desc in roles:
        exists = (
            db.query(TeacherRole)
            .filter(TeacherRole.code == code)
            .first()
        )

        if exists:
            skipped += 1
        else:
            db.add(TeacherRole(code=code, description=desc))
            created += 1

    db.commit()
    db.close()

    print(f"✅ TeacherRoles cargados | created={created} skipped={skipped}")


if __name__ == "__main__":
    run()