from sqlalchemy import Column, Integer, Float, ForeignKey
from database import Base

class GradePolicy(Base):
    __tablename__ = "grade_policies"

    id = Column(Integer, primary_key=True, index=True)

    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    academic_year = Column(Integer, nullable=False)

    quiz_weight = Column(Float, nullable=False)
    homework_weight = Column(Float, nullable=False)
    classwork_weight = Column(Float, nullable=False)
    project_weight = Column(Float, nullable=False)
    test_weight = Column(Float, nullable=False)