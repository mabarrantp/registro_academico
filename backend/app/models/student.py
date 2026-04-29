from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    student_code = Column(String(20), unique=True, nullable=False)

    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)

    entry_year = Column(Integer, nullable=False)
    entry_grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    current_grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)

    active = Column(Boolean, default=True)

    # ✅ Relaciones
    entry_grade = relationship("Grade", foreign_keys=[entry_grade_id])
    current_grade = relationship("Grade", foreign_keys=[current_grade_id])
    enrollments = relationship("Enrollment", back_populates="student")