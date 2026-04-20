from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from app.database import Base

class QuarterGrade(Base):
    __tablename__ = "quarter_grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    quarter_id = Column(Integer, ForeignKey("quarters.id"), nullable=False)
    final_score = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "subject_id",
            "quarter_id",
            name="uq_student_subject_quarter"
        ),
    )
