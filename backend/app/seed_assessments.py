from app.database import SessionLocal
from models.assessment import Assessment
from models.student import Student
from models.subject import Subject
from models.teacher import Teacher
from models.grade import Grade
from models.quarter import Quarter
from models.assessment_category import AssessmentCategory


def run():
    db = SessionLocal()

    def add(student_fn, subject_name, teacher_fn, grade_name, q_code, year, cat_code, score):
        student = db.query(Student).filter(Student.first_name == student_fn).first()
        subject = db.query(Subject).filter(Subject.name == subject_name).first()
        teacher = db.query(Teacher).filter(Teacher.first_name == teacher_fn).first()
        grade = db.query(Grade).filter(Grade.name == grade_name).first()
        quarter = db.query(Quarter).filter(
            Quarter.code == q_code,
            Quarter.academic_year == year
        ).first()
        category = db.query(AssessmentCategory).filter(
            AssessmentCategory.code == cat_code
        ).first()

        if not all([student, subject, teacher, grade, quarter, category]):
            return

        exists = (
            db.query(Assessment)
            .filter(
                Assessment.student_id == student.id,
                Assessment.subject_id == subject.id,
                Assessment.teacher_id == teacher.id,
                Assessment.grade_id == grade.id,
                Assessment.quarter_id == quarter.id,
                Assessment.category_id == category.id,
                Assessment.score == score,
            )
            .first()
        )

        if not exists:
            db.add(
                Assessment(
                    student_id=student.id,
                    subject_id=subject.id,
                    teacher_id=teacher.id,
                    grade_id=grade.id,
                    quarter_id=quarter.id,
                    category_id=category.id,
                    score=score,
                    on_time=True,
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


if __name__ == "__main__":
    run()