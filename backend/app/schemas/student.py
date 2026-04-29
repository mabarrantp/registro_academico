from pydantic import BaseModel


# ✅ Esquema para crear estudiante (uso normal / formulario)
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    entry_year: int
    entry_grade_id: int


# ✅ Esquema para importación masiva (Excel)
class StudentImportRow(BaseModel):
    first_name: str
    last_name: str
    entry_year: int
    entry_grade_id: int