from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from modules.auth.dependencies import get_current_admin
from modules.auth.models import User
from modules.admin.dto import DashboardMetrics
from modules.admin.service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/metrics", response_model=DashboardMetrics)
def get_metrics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Return platform-wide aggregate stats.
    Requires the requesting user to have is_admin = true.
    """
    return AdminService(db).get_metrics()
