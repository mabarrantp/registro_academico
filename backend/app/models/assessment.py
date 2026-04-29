from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True)

    # Relación con la asignación docente
    teacher_assignment_id = Column(
        Integer,
        ForeignKey("teacher_assignments.id"),
        nullable=False,
    )

    # Estudiante evaluado
    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
    )

    # Quarter (1, 2, 3, 4)
    quarter = Column(Integer, nullable=False)

    # Tipo de evaluación (QUIZ, EXAM, PROJECT, etc.)
    assessment_type = Column(String(50), nullable=False)

    # Nota (0–100)
    score = Column(Float, nullable=False)

    # Relaciones
    teacher_assignment = relationship("TeacherAssignment")
    student = relationship("Student")
