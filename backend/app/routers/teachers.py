from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from security import get_current_user, require_roles
from models.teacher import Teacher

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("")
def list_teachers(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_roles("ADMIN", "COORDINATION")(user)
    return db.query(Teacher).all()


@router.post("")
def create_teacher(
    first_name: str,
    last_name: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_roles("ADMIN", "COORDINATION")(user)

    teacher = Teacher(
        first_name=first_name,
        last_name=last_name,
        active=True
    )

    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher