from sqlalchemy import Column, Integer, String
from database import Base

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)   # Ej: 1°, 7°
    level = Column(String, nullable=False)               # PRIMARIA | SECUNDARIA