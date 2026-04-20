from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "grade_id",
            "academic_year",
            name="uq_student_grade_year"
        ),
    )
