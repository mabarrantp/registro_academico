from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from app.database import Base


class GradePolicy(Base):
    __tablename__ = "grade_policies"

    id = Column(Integer, primary_key=True, index=True)

    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    quarter_id = Column(Integer, ForeignKey("quarters.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)

    quiz_weight = Column(Float, nullable=False)
    homework_weight = Column(Float, nullable=False)
    classwork_weight = Column(Float, nullable=False)
    project_weight = Column(Float, nullable=False)
    test_weight = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "teacher_id",
            "subject_id",
            "grade_id",
            "quarter_id",
            "academic_year",
            name="uq_policy_teacher_subject_grade_quarter_year",
        ),
    )