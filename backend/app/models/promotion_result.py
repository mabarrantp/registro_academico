from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class PromotionResult(Base):
    __tablename__ = "promotion_results"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)

    # PROMOTED | RETAINED
    status = Column(String(20), nullable=False)

    failed_subjects = Column(Integer, nullable=False)

    student = relationship("Student")

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "academic_year",
            name="uq_student_year_promotion"
        ),
    )
