from database import SessionLocal
from models.grade_policy import GradePolicy
from models.subject import Subject
from models.grade import Grade

def run():
    db = SessionLocal()
    ACADEMIC_YEAR = 2025

    POLICIES = [
        ("Language Arts", "10°", 0.20, 0.20, 0.20, 0.20, 0.20),
        ("Math",          "10°", 0.15, 0.15, 0.20, 0.10, 0.40),
    ]

    created = skipped = missing = 0

    for subj_name, grade_name, qw, hw, cw, pw, tw in POLICIES:
        subject = db.query(Subject).filter(Subject.name == subj_name).first()
        grade = db.query(Grade).filter(Grade.name == grade_name).first()

        if not subject or not grade:
            missing += 1
            continue

        exists = db.query(GradePolicy).filter(
            GradePolicy.subject_id == subject.id,
            GradePolicy.grade_id == grade.id,
            GradePolicy.academic_year == ACADEMIC_YEAR
        ).first()

        if exists:
            skipped += 1
        else:
            db.add(
                GradePolicy(
                    subject_id=subject.id,
                    grade_id=grade.id,
                    academic_year=ACADEMIC_YEAR,
                    quiz_weight=qw,
                    homework_weight=hw,
                    classwork_weight=cw,
                    project_weight=pw,
                    test_weight=tw,
                )
            )
            created += 1

    db.commit()
    db.close()
    print(f"✅ GradePolicies seeded | created={created} skipped={skipped} missing={missing}")

if __name__ == "__main__":
    run()