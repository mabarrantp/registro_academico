from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    student_code: str      # se usa en UI
    grade_id: int
    section_id: int
    academic_year: int
