from sqlalchemy import Column, Integer, String
from database import Base

class Quarter(Base):
    __tablename__ = "quarters"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)          # QI, QII, QIII, QIV
    academic_year = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="OPEN")  # OPEN | CLOSED