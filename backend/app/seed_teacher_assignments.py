from app.database import SessionLocal
from app.models.teacher import Teacher
from app.models.subject import Subject
from app.models.teacher_role import TeacherRole
from app.models.teacher_assignment import TeacherAssignment

db = SessionLocal()

def assign(teacher_name, subject_name, grade_id, year, role_code):
    teacher = db.query(Teacher).filter(Teacher.first_name == teacher_name).first()
    subject = db.query(Subject).filter(Subject.name == subject_name).first()
    role = db.query(TeacherRole).filter(TeacherRole.code == role_code).first()
    if teacher and subject and role:
        exists = (
            db.query(TeacherAssignment)
            .filter(
                TeacherAssignment.teacher_id == teacher.id,
                TeacherAssignment.subject_id == subject.id,
                TeacherAssignment.grade_id == grade_id,
                TeacherAssignment.academic_year == year,
                TeacherAssignment.role_id == role.id,
            )
            .first()
        )
        if not exists:
            db.add(
                TeacherAssignment(
                    teacher_id=teacher.id,
                    subject_id=subject.id,
                    grade_id=grade_id,
                    academic_year=year,
                    role_id=role.id,
                )
            )

# === EJEMPLOS ===
# Rosa – 7° – Matemática y Física
assign("Rosa", "Math", 7, 2025, "SUBJECT_TEACHER")
assign("Rosa", "Physics", 7, 2025, "SUBJECT_TEACHER")

# Edwin – Secundaria – Ciencias
assign("Edwin", "Biology", 8, 2025, "SUBJECT_TEACHER")
assign("Edwin", "Chemistry", 9, 2025, "SUBJECT_TEACHER")
assign("Edwin", "Science", 7, 2025, "SUBJECT_TEACHER")

# María – Primaria – Maestra guía (varias materias)
assign("María", "Math", 3, 2025, "GUIDE_TEACHER")
assign("María", "Lengua y Literatura", 3, 2025, "GUIDE_TEACHER")
assign("María", "Estudios Sociales", 3, 2025, "GUIDE_TEACHER")

# Marcos – Computación – todos los grados (ejemplo)
assign("Marcos", "Computer", 1, 2025, "COMPLEMENTARY_TEACHER")
assign("Marcos", "Computer", 2, 2025, "COMPLEMENTARY_TEACHER")

db.commit()
db.close()

print("✅ TeacherAssignments cargados")
