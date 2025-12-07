from sqlalchemy.orm import Session
from app.models.activity_logs import ActivityLog
from app.schemas.activity_logs import ActivityLogCreate
from app.core.logging_config import logger


class ActivityLogService:
    @staticmethod
    def log_action(db: Session, data: ActivityLogCreate) -> ActivityLog:
        logger.info(
            f"Activity log | actor_type={data.actor_type} actor_id={data.actor_id} "
            f"action={data.action} entity_type={data.entity_type} entity_id={data.entity_id}"
        )

        log = ActivityLog(
            actor_type = data.actor_type,
            actor_id = data.actor_id,
            action = data.action,
            entity_type = data.entity_type,
            entity_id = data.entity_id,
            metadata = data.metadata,
        )

        db.add(log)
        db.commit()
        db.refresh(log)
    
        return log

    @staticmethod
    def list_logs(
        db: Session,
        actor_type: str | None = None,
        entity_type: str | None = None,
        entity_id: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ):
        
        q = db.query(ActivityLog)

        if actor_type:
            q = q.filter(ActivityLog.actor_type == actor_type)

        if entity_type:
            q = q.filter(ActivityLog.entity_type == entity_type)

        if entity_id is not None:
            q = q.filter(ActivityLog.entity_id == entity_id)

        q = q.order_by(ActivityLog.id.desc())
        return q.offset(offset).limit(limit).all()