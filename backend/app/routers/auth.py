from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from jose import jwt
import secrets

from app.database import get_db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.settings import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE,
    REFRESH_TOKEN_EXPIRE,
)
from app.core.auth import get_current_user
from app.core.rate_limit import check_login_rate_limit

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# ======================
# Helpers
# ======================

def create_access_token(user: User):
    payload = {
        "sub": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRE,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ======================
# Login (con Rate‑Limit)
# ======================

@router.post("/login")
def login(
    request: Request,
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    ip = request.client.host

    try:
        check_login_rate_limit(ip)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user or not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(user)

    refresh_token_value = secrets.token_urlsafe(48)
    refresh_token = RefreshToken(
        token=refresh_token_value,
        user_id=user.id,
        expires_at=datetime.utcnow() + REFRESH_TOKEN_EXPIRE
    )

    db.add(refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_value,
        "token_type": "bearer"
    }


# ======================
# Refresh Token (rotación)
# ======================

@router.post("/refresh")
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token)
        .first()
    )

    if not token or token.revoked_at or token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    user = db.query(User).get(token.user_id)

    # 🔁 rotar token
    token.revoked_at = datetime.utcnow()

    new_refresh_value = secrets.token_urlsafe(48)
    new_refresh = RefreshToken(
        token=new_refresh_value,
        user_id=user.id,
        expires_at=datetime.utcnow() + REFRESH_TOKEN_EXPIRE
    )

    db.add(new_refresh)
    db.commit()

    return {
        "access_token": create_access_token(user),
        "refresh_token": new_refresh_value,
        "token_type": "bearer"
    }


# ======================
# Logout GLOBAL
# ======================

@router.post("/logout")
def logout(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id,
        RefreshToken.revoked_at.is_(None)
    ).update(
        {RefreshToken.revoked_at: datetime.utcnow()},
        synchronize_session=False
    )

    db.commit()

    return {"detail": "Session closed on all devices"}


# ======================
# Me
# ======================

@router.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }
