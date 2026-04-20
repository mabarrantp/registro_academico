from pydantic import BaseModel
from typing import Optional

class AssessmentCreate(BaseModel):
    student_id: int
    subject_id: int
    teacher_id: int
    grade_id: int
    quarter_id: int
    category_id: int
    score: float
    on_time: bool = True
    comments: Optional[str] = None

class AssessmentOut(BaseModel):
    id: int
    student_id: int
    subject_id: int
    teacher_id: int
    grade_id: int
    quarter_id: int
    category_id: int
    score: float
    on_time: bool
    comments: Optional[str] = None
    status: str

    # Pydantic v2 (FastAPI actual)
    model_config = {"from_attributes": True}from pydantic import BaseModel
from typing import Optional

class AssessmentCreate(BaseModel):
    student_id: int
    subject_id: int
    teacher_id: int
    grade_id: int
    quarter_id: int
    category_id: int
    score: float
    on_time: bool = True
    comments: Optional[str] = None

class AssessmentOut(BaseModel):
    id: int
    student_id: int
    subject_id: int
    teacher_id: int
    grade_id: int
    quarter_id: int
    category_id: int
    score: float
    on_time: bool
    comments: Optional[str] = None
    status: str

    # ✅ Pydantic v2: permite serializar SQLAlchemy ORM
    model_config = {"from_attributes": True}