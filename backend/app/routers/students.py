from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.student import Student
from security import get_current_user, require_roles

router = APIRouter(prefix="/students", tags=["Students"])

ALLOWED_WRITE = ("ADMIN", "COORDINATION")


def norm_code(value: str) -> str:
    return value.strip().upper().replace(" ", "")


@router.post("/")
def create_student(
    local_code: str,
    first_name: str,
    last_name: str,
    mined_id: str | None = None,
    active: bool = True,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_roles(*ALLOWED_WRITE)(user)

    local_code_norm = norm_code(local_code)
    if not local_code_norm:
        raise HTTPException(400, "local_code is required")

    mined_norm = norm_code(mined_id) if mined_id else None

    # Duplicado por local_code
    exists_code = db.query(Student).filter(Student.local_code == local_code_norm).first()
    if exists_code:
        raise HTTPException(400, "local_code already exists")

    # Duplicado por mined_id si viene
    if mined_norm:
        exists_mined = db.query(Student).filter(Student.mined_id == mined_norm).first()
        if exists_mined:
            raise HTTPException(400, "mined_id already exists")

    student = Student(
        local_code=local_code_norm,
        mined_id=mined_norm,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        active=active
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/")
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.get("/by-code/{local_code}")
def get_by_local_code(local_code: str, db: Session = Depends(get_db)):
    code = norm_code(local_code)
    s = db.query(Student).filter(Student.local_code == code).first()
    if not s:
        raise HTTPException(404, "Student not found")
    return s


@router.get("/by-mined/{mined_id}")
def get_by_mined(mined_id: str, db: Session = Depends(get_db)):
    mid = norm_code(mined_id)
    s = db.query(Student).filter(Student.mined_id == mid).first()
    if not s:
        raise HTTPException(404, "Student not found")
    return s
