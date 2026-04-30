from typing import Optional, List
from pydantic import BaseModel, Field


# =====================================================
# Grade row (detalle de una nota)
# =====================================================

class GradeItemSchema(BaseModel):
    student: str = Field(
        ...,
        description="Nombre completo del estudiante",
        example="Juan Pérez",
    )
    grade: str = Field(
        ...,
        description="Grado o sección académica",
        example="Third Grade",
    )
    subject: str = Field(
        ...,
        description="Asignatura evaluada",
        example="Mathematics",
    )
    quarter: str = Field(
        ...,
        description="Quarter académico (Q1, Q2, Q3, Q4)",
        example="Q1",
    )
    quantitative: Optional[float] = Field(
        None,
        description="Nota cuantitativa",
        example=88,
    )
    qualitative: str = Field(
        "",
        description="Nota cualitativa (AA, AS, AF, AI)",
        example="AS",
    )


# =====================================================
# Response: listado de notas
# =====================================================

class GradesResponseSchema(BaseModel):
    grades: List[GradeItemSchema] = Field(
        ...,
        description="Listado de notas según los filtros aplicados",
    )


# =====================================================
# Response: promedio final por estudiante
# =====================================================

class FinalAverageSchema(BaseModel):
    student: str = Field(
        ...,
        description="Nombre completo del estudiante",
        example="Juan Pérez",
    )
    final_average: Optional[float] = Field(
        None,
        description="Promedio final del estudiante",
        example=84.75,
    )
    final_qualitative: str = Field(
        "",
        description="Evaluación cualitativa final",
        example="AS",
    )

