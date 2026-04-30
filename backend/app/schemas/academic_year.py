from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from app.models.academic_year import AcademicYearStatus


class AcademicYearCreate(BaseModel):
    """
    Payload para crear un Ciclo Lectivo.
    """
    name: str
    start_date: date
    end_date: date


class AcademicYearResponse(BaseModel):
    """
    Respuesta institucional del Ciclo Lectivo.
    """
    id: int
    name: str
    start_date: date
    end_date: date
    status: AcademicYearStatus
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    class Config:
        orm_mode = True
