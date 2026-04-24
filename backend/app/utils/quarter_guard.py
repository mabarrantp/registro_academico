from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.quarter import Quarter

def ensure_quarter_open(db: Session, quarter_id: int):
    q = db.query(Quarter).filter(Quarter.id == quarter_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quarter not found")
    if q.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail=f"Quarter {q.code} is CLOSED. No modifications allowed."
        )