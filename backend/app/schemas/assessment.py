from pydantic import BaseModel


class AssessmentCreate(BaseModel):
    teacher_assignment_id: int
    student_id: int
    quarter: int
    assessment_type: str
    score: float