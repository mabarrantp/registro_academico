from app.database import SessionLocal
from app.models.assessment import Assessment
from app.models.student import Student
from app.models.subject import Subject
from app.models.teacher import Teacher
from app.models.grade import Grade
from app.models.quarter import Quarter
from app.models.assessment_category import AssessmentCategory

db = SessionLocal()

def add(student_fn, subject_name, teacher_fn, grade_name, q_code, year, cat_code, score):
    student = db.query(Student).filter(Student.first_name == student_fn).first()
    subject = db.query(Subject).filter(Subject.name == subject_name).first()
    teacher = db.query(Teacher).filter(Teacher.first_name == teacher_fn).first()
    grade = db.query(Grade).filter(Grade.name == grade_name).first()
    quarter = db.query(Quarter).filter(Quarter.code == q_code, Quarter.academic_year == year).first()
    category = db.query(AssessmentCategory).filter(AssessmentCategory.code == cat_code).first()

    if all([student, subject, teacher, grade, quarter, category]):
        db.add(
            Assessment(
                student_id=student.id,
                subject_id=subject.id,
                teacher_id=teacher.id,
                grade_id=grade.id,
                quarter_id=quarter.id,
                category_id=category.id,
                score=score,
            )
        )

# === EJEMPLO: Language Arts – QI – 10° ===
add("Juan", "Language Arts", "Ana", "10°", "QI", 2025, "QUIZ", 85)
add("Juan", "Language Arts", "Ana", "10°", "QI", 2025, "QUIZ", 90)
add("Juan", "Language Arts", "Ana", "10°", "QI", 2025, "HOMEWORK", 88)
add("Juan", "Language Arts", "Ana", "10°", "QI", 2025, "CLASSWORK", 92)
add("Juan", "Language Arts", "Ana", "10°", "QI", 2025, "PROJECT", 95)
add("Juan", "Language Arts", "Ana", "10°", "QI", 2025, "TEST", 87)

db.commit()
db.close()

print("✅ Assessments cargados")