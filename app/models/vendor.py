from sqlalchemy import Column, Integer, String, DateTime, func
from app.database.connection import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    phone = Column(String, unique=True, nullable=False)
    company_name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())

    