from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False)

    # ✅ RELACIÓN CON DOCENTE
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
