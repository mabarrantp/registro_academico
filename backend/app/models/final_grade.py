from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base

class FinalGrade(Base):
    __tablename__ = "final_grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)
    final_score = Column(Float, nullable=False)