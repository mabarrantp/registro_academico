from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean, String
from app.database import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    quarter_id = Column(Integer, ForeignKey("quarters.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("assessment_categories.id"), nullable=False)

    score = Column(Float, nullable=False)
    on_time = Column(Boolean, default=True)
    comments = Column(String, nullable=True)

    # ✅ NUEVO: estado de la actividad
    status = Column(String, nullable=False, default="ACTIVE")  # ACTIVE | EXCLUDED