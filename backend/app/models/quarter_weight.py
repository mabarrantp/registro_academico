from sqlalchemy import Column, Integer, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class QuarterWeight(Base):
    __tablename__ = "quarter_weights"

    id = Column(Integer, primary_key=True, index=True)

    quarter_id = Column(
        Integer,
        ForeignKey("quarters.id"),
        nullable=False
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False
    )

    section_id = Column(
        Integer,
        ForeignKey("sections.id"),
        nullable=False
    )

    # ✅ Pesos definidos por el docente
    # Ejemplo:
    # {
    #   "QUIZZES": 0.2,
    #   "HOMEWORK": 0.1,
    #   "CLASSWORK": 0.3,
    #   "TEST": 0.4,
    #   "PROJECT": 0.0
    # }
    weights = Column(JSON, nullable=False)

    quarter = relationship("Quarter")
    subject = relationship("Subject")
    section = relationship("Section")

    __table_args__ = (
        UniqueConstraint(
            "quarter_id",
            "subject_id",
            "section_id",
            name="uq_quarter_subject_section_weights"
        ),
    )
