# Importa TODOS los modelos aquí para registrarlos en Base.metadata
# Orden: primero tablas "base" (subjects, grades, quarters), luego las que dependen de ellas.

from models.user import User
from models.audit_log import AuditLog

from models.teacher import Teacher
from models.teacher_role import TeacherRole
from models.teacher_specialty import TeacherSpecialty
from models.teacher_assignment import TeacherAssignment

from models.subject import Subject
from models.grade import Grade
from models.student import Student
from models.section import Section   # ✅ NUEVO (poner antes de Enrollment)
from models.enrollment import Enrollment

from models.quarter import Quarter
from models.assessment_category import AssessmentCategory

from models.grade_policy import GradePolicy
from models.assessment import Assessment
from models.quarter_grade import QuarterGrade
from models.final_grade import FinalGrade
