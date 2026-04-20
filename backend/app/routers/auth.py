from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(username: str, password: str, role: str, db: Session = Depends(get_db)):
    if role not in ["TEACHER", "COORDINATION", "ADMIN"]:
        raise HTTPException(400, "Invalid role")

    exists = db.query(User).filter(User.username == username).first()
    if exists:
        raise HTTPException(400, "Username already exists")

    user = User(
        username=username,
        hashed_password=hash_password(password),
        role=role,
        active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "role": user.role}

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username, User.active == True).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "role": user.role}