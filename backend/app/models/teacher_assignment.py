from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class TeacherAssignment(Base):
    __tablename__ = "teacher_assignments"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    grade_id = Column(Integer, nullable=False)      # módulo de grados vendrá después
    academic_year = Column(Integer, nullable=False)
    role_id = Column(Integer, ForeignKey("teacher_roles.id"), nullable=False)
