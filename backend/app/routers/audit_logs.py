from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.audit_log import AuditLog
from security import get_current_user, require_roles

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)

ALLOWED_ROLES = ("ADMIN", "COORDINATION")


@router.get("/")
def list_audit_logs(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    require_roles(*ALLOWED_ROLES)(user)
    return db.query(AuditLog).all()