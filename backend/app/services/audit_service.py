from sqlalchemy.orm import Session
from models.audit_log import AuditLog

def log_event(
    db: Session,
    entity_type: str,
    entity_id: int,
    action: str,
    performed_by: str,
    old_value: str | None = None,
    new_value: str | None = None,
    comment: str | None = None,
):
    log = AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        old_value=old_value,
        new_value=new_value,
        performed_by=performed_by,
        comment=comment,
    )
    db.add(log)
    db.commit()
