from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class AcademicRecordSignature(Base):
    __tablename__ = "academic_record_signatures"

    id = Column(Integer, primary_key=True, index=True)

    academic_record_id = Column(
        Integer,
        ForeignKey("academic_records.id"),
        nullable=False
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # DIRECTOR | COORDINATION | GUIDE_TEACHER
    role = Column(String(30), nullable=False)

    signed_at = Column(DateTime, default=datetime.utcnow)

    academic_record = relationship("AcademicRecord")
    user = relationship("User")

    __table_args__ = (
        UniqueConstraint(
            "academic_record_id",
            "role",
            name="uq_record_role_signature"
        ),
    )