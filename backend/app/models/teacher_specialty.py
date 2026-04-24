from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class TeacherSpecialty(Base):
    __tablename__ = "teacher_specialties"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)