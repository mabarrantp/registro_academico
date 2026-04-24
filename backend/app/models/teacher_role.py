from sqlalchemy import Column, Integer, String
from database import Base

class TeacherRole(Base):
    __tablename__ = "teacher_roles"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
