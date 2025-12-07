from pydantic import BaseModel
from datetime import datetime

class ActivityLogBase(BaseModel):
    actor_type: str
    actor_id: int | None = None
    action: str
    entity_type: str
    entity_id: int
    metadata: str | None = None


class ActivityLogCreate(ActivityLogBase):
    pass


class ActivityLogResponse(ActivityLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
