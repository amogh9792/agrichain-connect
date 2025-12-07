from sqlalchemy import Column, Integer, String, DateTime, Text, func
from app.database.connection import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index= True)

    actor_type = Column(String, nullable=False)
    actor_id = Column(Integer, nullable=False)

    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)

    meta_info = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

