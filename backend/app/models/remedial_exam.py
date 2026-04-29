from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class RemedialExam(Base):
    __tablename__ = "remedial_exams"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)

    score = Column(Float, nullable=False)

    student = relationship("Student")
    subject = relationship("Subject")

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "subject_id",
            "academic_year",
            name="uq_student_subject_year_remedial"
        ),
    )