from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    code = Column(String(5), nullable=False)
    active = Column(Boolean, default=True)

    # ✅ Relaciones
    grade = relationship("Grade", back_populates="sections")
    enrollments = relationship("Enrollment", back_populates="section")