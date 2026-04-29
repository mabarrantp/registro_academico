from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
import tempfile

from app.database import get_db
from security import get_current_user, require_roles

from models.academic_record import AcademicRecord
from models.guide_teacher_assignment import GuideTeacherAssignment
from models.enrollment import Enrollment
from models.student import Student
from models.promotion_result import PromotionResult
from models.grade import Grade
from models.section import Section
from models.teacher import Teacher

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas


router = APIRouter(prefix="/exports", tags=["Exports"])


@router.get("/academic-record/pdf")
def export_academic_record_pdf(
    grade_id: int,
    section_id: int,
    academic_year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Genera el PDF oficial del Acta Académica.
    Permite: ADMIN, COORDINATION, DIRECTOR, GUIDE_TEACHER
    """
    # ✅ Ahora permitimos GUIDE_TEACHER
    require_roles("ADMIN", "COORDINATION", "DIRECTOR", "GUIDE_TEACHER")(user)

    # ✅ Validación extra: si es maestro guía, debe ser guía de ese grupo/año
    if getattr(user, "role", None) == "GUIDE_TEACHER":
        guide = db.query(GuideTeacherAssignment).filter(
            GuideTeacherAssignment.grade_id == grade_id,
            GuideTeacherAssignment.section_id == section_id,
            GuideTeacherAssignment.academic_year == academic_year
        ).first()

        if not guide:
            raise HTTPException(status_code=403, detail="No asignado como Maestro Guía para este grupo/año.")

        # Si tu Teacher tiene relación con User (teacher.user_id), validamos:
        # (Si no tienes user_id en Teacher, comenta este bloque)
        teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
        if teacher and teacher.id != guide.teacher_id:
            raise HTTPException(status_code=403, detail="Este usuario no es el Maestro Guía asignado.")

    # -------------------------
    # Obtener datos base
    # -------------------------
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    section = db.query(Section).filter(Section.id == section_id).first()
    if not grade or not section:
        raise HTTPException(status_code=404, detail="Grado o sección no encontrada")

    guide = db.query(GuideTeacherAssignment).filter(
        GuideTeacherAssignment.grade_id == grade_id,
        GuideTeacherAssignment.section_id == section_id,
        GuideTeacherAssignment.academic_year == academic_year
    ).first()

    if not guide:
        raise HTTPException(status_code=404, detail="Maestro guía no asignado")

    guide_teacher = db.query(Teacher).filter(Teacher.id == guide.teacher_id).first()

    enrollments = db.query(Enrollment).filter(
        Enrollment.grade_id == grade_id,
        Enrollment.section_id == section_id,
        Enrollment.academic_year == academic_year
    ).all()

    # -------------------------
    # Crear PDF temporal
    # -------------------------
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=LETTER)

    width, height = LETTER

    # Encabezado
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 50, "ACTA ACADÉMICA OFICIAL")

    c.setFont("Helvetica", 11)
    c.drawString(50, height - 90, f"Año académico: {academic_year}")
    c.drawString(50, height - 110, f"Grado: {grade.name}")
    c.drawString(200, height - 110, f"Sección: {section.code}")

    guide_name = "N/D"
    if guide_teacher:
        guide_name = f"{guide_teacher.first_name} {guide_teacher.last_name}"
    c.drawString(50, height - 130, f"Maestro Guía: {guide_name}")

    # Tabla encabezado
    y = height - 170
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "No.")
    c.drawString(90, y, "Estudiante")
    c.drawString(350, y, "Resultado")

    c.setFont("Helvetica", 10)
    y -= 20

    count = 1

    for e in enrollments:
        student = db.query(Student).filter(Student.id == e.student_id).first()
        promo = db.query(PromotionResult).filter(
            PromotionResult.student_id == e.student_id,
            PromotionResult.academic_year == academic_year
        ).first()

        student_name = f"{student.first_name} {student.last_name}" if student else f"Student {e.student_id}"
        result = promo.status if promo else "N/A"

        c.drawString(50, y, str(count))
        c.drawString(90, y, student_name)
        c.drawString(350, y, result)

        y -= 18
        count += 1

        if y < 80:
            c.showPage()
            y = height - 80

    # Firmas
    c.setFont("Helvetica", 11)
    c.drawString(50, 80, "_____________________________")
    c.drawString(50, 65, "Firma Dirección")

    c.drawString(300, 80, "_____________________________")
    c.drawString(300, 65, "Firma Maestro Guía")

    c.drawString(50, 40, f"Fecha de emisión: {datetime.now().strftime('%d/%m/%Y')}")
    c.save()

    return FileResponse(
        tmp.name,
        filename=f"acta_{grade.name}_{section.code}_{academic_year}.pdf",
        media_type="application/pdf"
    )
