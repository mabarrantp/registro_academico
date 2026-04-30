from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import require_admin
from app.services.academic_year_service import close_active_academic_year
from app.services.audit_log_service import log_action

router = APIRouter(
    prefix="/admin/closure",
    tags=["Academic Closure"]
)

@router.post("/close-year")
def close_year(
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    year = close_active_academic_year(db)
    log_action(
        db=db,
        user_id=admin.id,
        action="CLOSE_ACADEMIC_YEAR",
        details=f"Closed academic year {year.id}"
    )
    return {"status": "closed", "academic_year_id": year.id}
