from typing import Optional
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from security import get_current_user, require_roles

from models.final_subject_grade import FinalSubjectGrade
from models.promotion_result import PromotionResult
from models.enrollment import Enrollment
from models.student import Student
from models.grade import Grade
from models.section import Section


router = APIRouter(
    prefix="/promotion",
    tags=["Promotion"]
)

MAX_FAILED_SUBJECTS = 3


# =====================================================
# POST /promotion/run
# Ejecuta promoción final del año académico
# =====================================================
@router.post("/run")
def run_promotion(
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Ejecuta la promoción final del año académico:
    - Lee final_subject_grades
    - Aplica límite de materias reprobadas (MAX_FAILED_SUBJECTS)
    - Guarda PromotionResult
    - Si PROMOTED: crea Enrollment para el año siguiente (grado siguiente, sección A)
    """
    require_roles("ADMIN", "COORDINATION")(user)

    grades = db.query(FinalSubjectGrade).filter(
        FinalSubjectGrade.academic_year == academic_year
    ).all()

    # Agrupar por estudiante
    by_student = defaultdict(list)
    for g in grades:
        by_student[g.student_id].append(g)

    promoted = 0
    retained = 0

    for student_id, subjects in by_student.items():

        # Materias reprobadas: FAILED o REMEDIAL
        failed_subjects = [s for s in subjects if s.status in ("FAILED", "REMEDIAL")]
        failed_count = len(failed_subjects)

        # Regla académica:
        # - Si > MAX_FAILED_SUBJECTS -> RETAINED
        # - Si alguna FAILED (aunque <=3) -> RETAINED
        # - Si no -> PROMOTED
        if failed_count > MAX_FAILED_SUBJECTS:
            status = "RETAINED"
            retained += 1
        elif any(s.status == "FAILED" for s in subjects):
            status = "RETAINED"
            retained += 1
        else:
            status = "PROMOTED"
            promoted += 1

        # Guardar/actualizar resultado
        existing = db.query(PromotionResult).filter(
            PromotionResult.student_id == student_id,
            PromotionResult.academic_year == academic_year
        ).first()

        if existing:
            existing.status = status
            existing.failed_subjects = failed_count
        else:
            db.add(PromotionResult(
                student_id=student_id,
                academic_year=academic_year,
                status=status,
                failed_subjects=failed_count
            ))

        # Si promueve -> crear matrícula año siguiente
        if status == "PROMOTED":
            current_enrollment = db.query(Enrollment).filter(
                Enrollment.student_id == student_id,
                Enrollment.academic_year == academic_year
            ).first()

            if current_enrollment:
                # Buscar grado siguiente
                next_grade = db.query(Grade).filter(
                    Grade.id == (current_enrollment.grade_id + 1)
                ).first()

                if next_grade:
                    # Buscar sección A del año siguiente para ese grado
                    next_section = db.query(Section).filter(
                        Section.grade_id == next_grade.id,
                        Section.code == "A",
                        Section.academic_year == (academic_year + 1)
                    ).first()

                    if next_section:
                        # Evitar duplicado
                        exists_next = db.query(Enrollment).filter(
                            Enrollment.student_id == student_id,
                            Enrollment.academic_year == (academic_year + 1)
                        ).first()

                        if not exists_next:
                            db.add(Enrollment(
                                student_id=student_id,
                                grade_id=next_grade.id,
                                section_id=next_section.id,
                                academic_year=(academic_year + 1)
                            ))

    db.commit()

    return {
        "academic_year": academic_year,
        "promoted": promoted,
        "retained": retained
    }


# =====================================================
# GET /promotion/results
# Lista resultados de promoción (con filtros)
# =====================================================
@router.get("/results")
def get_promotion_results(
    academic_year: int,
    grade_id: Optional[int] = None,
    section_id: Optional[int] = None,
    status: Optional[str] = None,  # PROMOTED | RETAINED
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Lista resultados de promoción.

    Requerido:
    - academic_year

    Opcionales:
    - grade_id
    - section_id
    - status: PROMOTED | RETAINED

    Devuelve:
    - student_id, local_code, student_name, failed_subjects, status, academic_year
    """
    require_roles("ADMIN", "COORDINATION", "TEACHER", "GUIDE_TEACHER")(user)

    q = (
        db.query(PromotionResult, Student)
        .join(Student, Student.id == PromotionResult.student_id)
        .filter(PromotionResult.academic_year == academic_year)
    )

    # Filtro por status
    if status:
        status_norm = status.strip().upper()
        if status_norm not in ("PROMOTED", "RETAINED"):
            raise HTTPException(
                status_code=400,
                detail="status inválido (PROMOTED | RETAINED)"
            )
        q = q.filter(PromotionResult.status == status_norm)

    # Filtro por grado/sección usando Enrollment del mismo año
    if grade_id is not None or section_id is not None:
        q = q.join(
            Enrollment,
            (Enrollment.student_id == PromotionResult.student_id) &
            (Enrollment.academic_year == academic_year)
        )

        if grade_id is not None:
            q = q.filter(Enrollment.grade_id == grade_id)

        if section_id is not None:
            q = q.filter(Enrollment.section_id == section_id)

    rows = q.all()

    return [
        {
            "student_id": pr.student_id,
            "local_code": st.local_code,
            "student_name": f"{st.first_name} {st.last_name}",
            "academic_year": pr.academic_year,
            "failed_subjects": pr.failed_subjects,
            "status": pr.status
        }
        for pr, st in rows
    ]
