from database import SessionLocal
from models.teacher import Teacher
from models.subject import Subject
from models.teacher_role import TeacherRole
from models.teacher_assignment import TeacherAssignment
from models.grade import Grade
from models.section import Section


def run():
    db = SessionLocal()
    YEAR = 2025
    DEFAULT_SECTION_CODE = "A"  # si hoy solo hay una sección por grado, usa "A"

    def get_section_id(grade_name: str, year: int, code: str) -> int | None:
        grade = db.query(Grade).filter(Grade.name == grade_name).first()
        if not grade:
            return None

        section = (
            db.query(Section)
            .filter(
                Section.grade_id == grade.id,
                Section.academic_year == year,
                Section.code == code
            )
            .first()
        )
        return section.id if section else None

    def assign(teacher_first_name: str, subject_name: str | None, grade_name: str, year: int, role_code: str, section_code: str = DEFAULT_SECTION_CODE):
        teacher = db.query(Teacher).filter(Teacher.first_name == teacher_first_name).first()
        role = db.query(TeacherRole).filter(TeacherRole.code == role_code).first()
        section_id = get_section_id(grade_name, year, section_code)

        if not teacher or not role or not section_id:
            return

        # Para guía: no lleva materia
        subject_id = None
        if role_code != "GUIDE_TEACHER":
            if not subject_name:
                return
            subject = db.query(Subject).filter(Subject.name == subject_name).first()
            if not subject:
                return
            subject_id = subject.id

        # Evitar duplicado exacto
        exists = db.query(TeacherAssignment).filter(
            TeacherAssignment.teacher_id == teacher.id,
            TeacherAssignment.section_id == section_id,
            TeacherAssignment.subject_id == subject_id,
            TeacherAssignment.role_id == role.id,
            TeacherAssignment.academic_year == year,
        ).first()

        if not exists:
            db.add(TeacherAssignment(
                teacher_id=teacher.id,
                section_id=section_id,
                subject_id=subject_id,
                academic_year=year,
                role_id=role.id
            ))

    # ==========================================
    # EJEMPLOS (ajusta a tu realidad)
    # ==========================================

    # Honorio guía de 11°A y da Spanish en 11°A
    assign("Honorio", None, "11°", YEAR, "GUIDE_TEACHER", "A")
    assign("Honorio", "Spanish", "11°", YEAR, "SUBJECT_TEACHER", "A")

    # Rosa da Math en 7°A (si 7° existe y sección A existe)
    assign("Rosa", "Math", "7°", YEAR, "SUBJECT_TEACHER", "A")

    # Marcos da Computer en 1°A como complementario
    assign("Marcos", "Computer", "1°", YEAR, "COMPLEMENTARY_TEACHER", "A")

    db.commit()
    db.close()
    print("✅ TeacherAssignments seeded (por sección)")


if __name__ == "__main__":
    run()
