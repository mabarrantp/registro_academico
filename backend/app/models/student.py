from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    active = Column(Boolean, default=True)