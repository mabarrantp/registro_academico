from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from database import Base

class TeacherAssignment(Base):
    __tablename__ = "teacher_assignments"

    id = Column(Integer, primary_key=True, index=True)

    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)

    # Para GUIDE_TEACHER puede ser NULL; para profesores de materia debe venir.
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)

    academic_year = Column(Integer, nullable=False)
    role_id = Column(Integer, ForeignKey("teacher_roles.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "teacher_id", "section_id", "subject_id", "role_id", "academic_year",
            name="uq_teacher_assign"
        ),
    )
