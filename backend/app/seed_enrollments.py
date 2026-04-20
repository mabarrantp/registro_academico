from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal

# ✅ carga TODOS los modelos en metadata (evita NoReferencedTableError)
from app.models import _load  # noqa: F401

from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.grade import Grade

db = SessionLocal()

ACADEMIC_YEAR = 2025

# (first_name, last_name, grade_name)
ENROLLMENTS = [
    ("Juan", "Pérez", "10°"),
    ("María", "Gómez", "10°"),
    ("Carlos", "López", "10°"),
]

created = 0
skipped = 0
missing = 0

for fn, ln, grade_name in ENROLLMENTS:
    student = db.query(Student).filter(
        Student.first_name == fn,
        Student.last_name == ln
    ).first()

    grade = db.query(Grade).filter(Grade.name == grade_name).first()

    if not student:
        print(f"⚠️ Student not found: {fn} {ln}")
        missing += 1
        continue

    if not grade:
        print(f"⚠️ Grade not found: {grade_name}")
        missing += 1
        continue

    exists = db.query(Enrollment).filter(
        Enrollment.student_id == student.id,
        Enrollment.grade_id == grade.id,
        Enrollment.academic_year == ACADEMIC_YEAR
    ).first()

    if exists:
        skipped += 1
        continue

    db.add(Enrollment(
        student_id=student.id,
        grade_id=grade.id,
        academic_year=ACADEMIC_YEAR
    ))

    try:
        db.commit()
        created += 1
    except IntegrityError as e:
        db.rollback()
        print(f"❌ Enrollment error {fn} {ln} -> {grade_name}: {e.orig}")
        skipped += 1

db.close()
print(f"✅ Enrollments seeded | created={created} skipped={skipped} missing={missing}")
