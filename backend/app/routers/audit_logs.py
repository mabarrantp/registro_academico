from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audit_log import AuditLog
from app.deps import require_roles

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

ALLOWED_ROLES = ("COORDINATION", "ADMIN")


@router.get("/", dependencies=[Depends(require_roles(*ALLOWED_ROLES))])
def list_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.performed_at.desc()).all()