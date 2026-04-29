import app.models  # fuerza carga de todos los modelos

from app.database import SessionLocal, Base, engine

from app.seed_grades import seed_grades
from app.seed_sections import seed_sections
from app.seed_subjects import seed_subjects
from app.seed_teachers import run as seed_teachers
from app.seed_users import seed_users
from app.seed_teacher_assignments import seed_teacher_assignments
from app.seed_quarters import seed_quarters


def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_grades(db)
        seed_sections(db)
        seed_subjects(db)
        seed_teachers(db)
        seed_users(db)
        seed_teacher_assignments(db)
        seed_quarters(db)  # ✅ AQUÍ
        print("✅ SEED COMPLETO FINALIZADO")
    finally:
        db.close()


if __name__ == "__main__":
    main()