from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class TeacherAssignment(Base):
    __tablename__ = "teacher_assignments"

    id = Column(Integer, primary_key=True)

    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "teacher_id",
            "subject_id",
            "section_id",
            "academic_year",
            name="uq_teacher_subject_section_year",
        ),
    )

    teacher = relationship("Teacher")
    subject = relationship("Subject")
    section = relationship("Section")
