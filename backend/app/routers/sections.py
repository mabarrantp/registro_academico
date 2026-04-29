from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.section import Section

router = APIRouter(prefix="/sections", tags=["Sections"])


@router.get("")
def list_sections(db: Session = Depends(get_db)):
    return (
        db.query(Section)
        .filter(Section.active == True)
        .all()
    )
