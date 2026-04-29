from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("student_id", "academic_year", name="uq_student_year"),
    )

    # ✅ Relaciones (strings, no imports directos)
    student = relationship("Student", back_populates="enrollments")
    grade = relationship("Grade", back_populates="enrollments")
    section = relationship("Section", back_populates="enrollments")