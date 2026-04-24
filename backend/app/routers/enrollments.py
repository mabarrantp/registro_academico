import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.enrollment import Enrollment
from models.student import Student
from models.grade import Grade
from models.section import Section

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


# ==========================
# Normalizadores
# ==========================
def normalize_mined_id(value: str) -> str:
    # trim + mayúsculas + elimina espacios internos
    return value.strip().upper().replace(" ", "")


def normalize_grade_name(value: str) -> str:
    """
    Acepta:
      - '10°'
      - '10'
      - '10th', '10th Grade', '10THGRADE'
      - '11°', '11th grade', etc.
    Devuelve siempre en formato DB actual: 'N°' (ej. '10°')
    """
    if value is None:
        return ""

    s = value.strip().upper().replace(" ", "")
    # Si ya viene como '10°'
    if "°" in s:
        # Ej: '10°' o '10°A' (si alguien se equivoca)
        m = re.match(r"^(\d{1,2})°", s)
        return f"{m.group(1)}°" if m else s

    # Extraer el número (ej: 10, 10TH, 10THGRADE)
    m = re.match(r"^(\d{1,2})", s)
    if not m:
        return ""

    n = int(m.group(1))
    if n < 1 or n > 12:
        # ajusta el rango según tu colegio (1..11 normalmente)
        return ""

    return f"{n}°"


# ==========================
# GET: listar enrollments
# ==========================
@router.get("/")
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()


# ==========================
# DELETE: borrar enrollment por id
# ==========================
@router.delete("/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    e = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    db.delete(e)
    db.commit()
    return {"status": "deleted", "enrollment_id": enrollment_id}


# ==========================
# DELETE: borrar enrollment por mined_id + grado + año (opcional pero útil)
# ==========================
@router.delete("/by-mined")
def delete_enrollment_by_mined(
    mined_id: str,
    grade_name: str,
    academic_year: int,
    db: Session = Depends(get_db),
):
    mined_id_norm = normalize_mined_id(mined_id)
    grade_name_norm = normalize_grade_name(grade_name)

    if not grade_name_norm:
        raise HTTPException(status_code=400, detail="Invalid grade_name")

    student = db.query(Student).filter(Student.mined_id == mined_id_norm).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found for that MINED ID")

    grade = db.query(Grade).filter(Grade.name == grade_name_norm).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    e = db.query(Enrollment).filter(
        Enrollment.student_id == student.id,
        Enrollment.grade_id == grade.id,
        Enrollment.academic_year == academic_year,
    ).first()

    if not e:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    db.delete(e)
    db.commit()
    return {"status": "deleted", "enrollment_id": e.id}


# ==========================
# POST: matrícula por MINED + grado + año, elige sección automáticamente
# IDempotente: si ya existe, devuelve 200 con already_enrolled=true
# ==========================
@router.post("/by-mined-auto")
def enroll_by_mined_auto(
    mined_id: str,
    grade_name: str,
    academic_year: int,
    preferred_section_code: str = "A",
    db: Session = Depends(get_db),
):
    # 1) normalizar entradas
    mined_id_norm = normalize_mined_id(mined_id)
    grade_name_norm = normalize_grade_name(grade_name)

    if not mined_id_norm:
        raise HTTPException(status_code=400, detail="mined_id is required")

    if not grade_name_norm:
        raise HTTPException(status_code=400, detail="Invalid grade_name")

    # 2) buscar estudiante
    student = db.query(Student).filter(Student.mined_id == mined_id_norm).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found for that MINED ID")

    # 3) buscar grado
    grade = db.query(Grade).filter(Grade.name == grade_name_norm).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    # 4) buscar secciones del grado/año
    sections = db.query(Section).filter(
        Section.grade_id == grade.id,
        Section.academic_year == academic_year
    ).all()

    if not sections:
        raise HTTPException(status_code=404, detail="No sections found for that grade/year")

    # 5) elegir sección automáticamente
    selected_section = None
    if len(sections) == 1:
        selected_section = sections[0]
    else:
        pref = preferred_section_code.strip().upper()
        selected_section = next((s for s in sections if s.code == pref), None)
        if not selected_section:
            options = sorted({s.code for s in sections})
            raise HTTPException(
                status_code=400,
                detail=f"Multiple sections exist. Send preferred_section_code. Available: {options}"
            )

    # 6) si ya existe enrollment -> IDempotente: devolver 200 con already_enrolled=true
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == student.id,
        Enrollment.grade_id == grade.id,
        Enrollment.academic_year == academic_year
    ).first()

    if existing:
        # si el modelo tiene section_id y aún no coincide, lo ajustamos (opcional)
        if hasattr(existing, "section_id") and existing.section_id != selected_section.id:
            existing.section_id = selected_section.id
            db.commit()
            db.refresh(existing)

        return {
            "already_enrolled": True,
            "enrollment": existing,
            "selected_section": {
                "id": selected_section.id,
                "code": selected_section.code,
                "name": selected_section.name,
                "grade_name": grade.name,
                "academic_year": selected_section.academic_year
            }
        }

    # 7) crear nuevo enrollment
    enrollment = Enrollment(
        student_id=student.id,
        grade_id=grade.id,
        academic_year=academic_year
    )

    if hasattr(enrollment, "section_id"):
        enrollment.section_id = selected_section.id

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return {
        "already_enrolled": False,
        "enrollment": enrollment,
        "selected_section": {
            "id": selected_section.id,
            "code": selected_section.code,
            "name": selected_section.name,
            "grade_name": grade.name,
            "academic_year": selected_section.academic_year
        }
    }
