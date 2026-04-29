from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)

    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)

    email = Column(String(120), unique=True, nullable=True)
    active = Column(Boolean, default=True)
