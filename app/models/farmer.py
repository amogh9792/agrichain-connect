from sqlalchemy import Column, Integer, String, DateTime, func
from app.database.connection import Base

class Farmer(Base):
    __tablename__ = "farmer"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    phone = Column(String, unique=True, nullable=False)
    location = Column(String)
    created_at = Column(DateTime, server_default=func.now())