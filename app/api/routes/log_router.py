from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.activity_logs import ActivityLogResponse
from app.services.log_servie import ActivityLogService

router = APIRouter(prefix="/activity", tags=["Activity Logs"])


@router.get("/logs", response_model=list[ActivityLogResponse])
def list_activity_logs(
    actor_type: str | None = Query(None),
    entity_type: str | None = Query(None),
    entity_id: int | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return ActivityLogService.list_logs(
        db,
        actor_type=actor_type,
        entity_type=entity_type,
        entity_id=entity_id,
        limit=limit,
        offset=offset,
    )
