from app.database import SessionLocal
from app.models.teacher_role import TeacherRole

db = SessionLocal()

roles = [
    ("GUIDE_TEACHER", "Maestro guía"),
    ("SUBJECT_TEACHER", "Profesor de asignatura"),
    ("COMPLEMENTARY_TEACHER", "Profesor complementario"),
]

for code, desc in roles:
    if not db.query(TeacherRole).filter(TeacherRole.code == code).first():
        db.add(TeacherRole(code=code, description=desc))

db.commit()
db.close()

print("✅ TeacherRoles cargados")