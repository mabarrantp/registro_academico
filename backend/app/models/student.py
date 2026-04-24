from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    # ✅ Código interno del colegio (viene de tu Excel: CODE)
    local_code = Column(String, unique=True, index=True, nullable=False)

    # ✅ Código oficial MINED / Registro General (opcional)
    mined_id = Column(String, unique=True, index=True, nullable=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
