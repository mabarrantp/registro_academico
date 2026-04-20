from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from app.models import _load  # noqa: F401

from app.models.grade_policy import GradePolicy

db = SessionLocal()

teacher_id = 1
subject_id = 1
grade_id = 2
quarter_id = 2
academic_year = 2025

# Pesos (deben sumar 1.0)
quiz = 0.20
homework = 0.20
classwork = 0.20
project = 0.20
test = 0.20

exists = db.query(GradePolicy).filter(
    GradePolicy.teacher_id == teacher_id,
    GradePolicy.subject_id == subject_id,
    GradePolicy.grade_id == grade_id,
    GradePolicy.quarter_id == quarter_id,
    GradePolicy.academic_year == academic_year,
).first()

if exists:
    print("ℹ️ GradePolicy ya existe (no se insertó).")
    db.close()
    raise SystemExit

db.add(GradePolicy(
    teacher_id=teacher_id,
    subject_id=subject_id,
    grade_id=grade_id,
    quarter_id=quarter_id,
    academic_year=academic_year,
    quiz_weight=quiz,
    homework_weight=homework,
    classwork_weight=classwork,
    project_weight=project,
    test_weight=test,
))

try:
    db.commit()
    print("✅ GradePolicy insertada correctamente.")
except IntegrityError as e:
    db.rollback()
    print(f"❌ Error insertando GradePolicy: {e.orig}")
finally:
    db.close()