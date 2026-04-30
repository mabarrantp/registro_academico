from typing import Dict, Optional, List
from pydantic import BaseModel, Field


# =====================================================
# Quarter grade (Q1, Q2, etc.)
# =====================================================

class QuarterGradeSchema(BaseModel):
    quantitative: Optional[float] = Field(
        None,
        description="Nota cuantitativa del quarter",
        example=85,
    )
    qualitative: str = Field(
        "",
        description="Nota cualitativa (AA, AS, AF, AI)",
        example="AS",
    )


# =====================================================
# Subject row in report card
# =====================================================

class ReportCardSubjectSchema(BaseModel):
    subject: str = Field(
        ...,
        description="Nombre de la asignatura",
        example="Mathematics",
    )
    grade: str = Field(
        ...,
        description="Grado o nivel académico",
        example="Third Grade",
    )
    quarters: Dict[str, QuarterGradeSchema] = Field(
        ...,
        description="Notas por quarter (Q1, Q2, Q3, Q4)",
        example={
            "Q1": {"quantitative": 88, "qualitative": "AS"},
            "Q2": {"quantitative": 91, "qualitative": "AA"},
        },
    )
    final_average: Optional[float] = Field(
        None,
        description="Promedio final de la asignatura",
        example=89.5,
    )
    final_qualitative: str = Field(
        "",
        description="Cualitativo final (AA, AS, AF, AI)",
        example="AS",
    )


# =====================================================
# Report Card response (root)
# =====================================================

class ReportCardResponseSchema(BaseModel):
    student: str = Field(
        ...,
        description="Nombre completo del estudiante",
        example="Juan Pérez",
    )
    academic_year: int = Field(
        ...,
        description="Año académico",
        example=2026,
    )
    report_card: List[ReportCardSubjectSchema] = Field(
        ...,
        description="Listado de asignaturas con sus notas",
    )
