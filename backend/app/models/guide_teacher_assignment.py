from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class GuideTeacherAssignment(Base):
    __tablename__ = "guide_teacher_assignments"

    id = Column(Integer, primary_key=True, index=True)

    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)

    teacher = relationship("Teacher")
    grade = relationship("Grade")
    section = relationship("Section")

    __table_args__ = (
        UniqueConstraint(
            "grade_id",
            "section_id",
            "academic_year",
            name="uq_guide_teacher_per_section_year"
        ),
    )
