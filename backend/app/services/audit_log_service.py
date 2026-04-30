from app.models.audit_log import AuditLog


def log_action(db, user_id: int, action: str, details: str):
    entry = AuditLog(
        user_id=user_id,
        action=action,
        details=details
    )
    db.add(entry)
    db.commit()
