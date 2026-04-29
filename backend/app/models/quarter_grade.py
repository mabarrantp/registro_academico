from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class QuarterGrade(Base):
    __tablename__ = "quarter_grades"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    quarter_id = Column(Integer, ForeignKey("quarters.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)

    final_grade = Column(Float, nullable=False)

    student = relationship("Student")
    subject = relationship("Subject")
    quarter = relationship("Quarter")

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "subject_id",
            "quarter_id",
            name="uq_student_subject_quarter_grade"
        ),
    )