from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class AcademicRecord(Base):
    __tablename__ = "academic_records"

    id = Column(Integer, primary_key=True, index=True)

    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)

    guide_teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    issued_at = Column(DateTime, default=datetime.utcnow)

    grade = relationship("Grade")
    section = relationship("Section")
    guide_teacher = relationship("Teacher")