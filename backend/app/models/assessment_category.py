from sqlalchemy import Column, Integer, String
from database import Base

class AssessmentCategory(Base):
    __tablename__ = "assessment_categories"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
