from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False, unique=True)
    order = Column(Integer, nullable=False)
    level = Column(String(20), nullable=False)
    label = Column(String(20), nullable=False)
    active = Column(Boolean, default=True)

    # ✅ Relaciones
    sections = relationship("Section", back_populates="grade")
    enrollments = relationship("Enrollment", back_populates="grade")