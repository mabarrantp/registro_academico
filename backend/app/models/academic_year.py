from sqlalchemy import Column, Integer, String, Date, DateTime, Enum
from sqlalchemy.sql import func
import enum

from app.database import Base


class AcademicYearStatus(str, enum.Enum):
    CREATED = "CREATED"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class AcademicYear(Base):
    __tablename__ = "academic_years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    status = Column(
        Enum(AcademicYearStatus),
        nullable=False,
        default=AcademicYearStatus.CREATED
    )

    opened_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

