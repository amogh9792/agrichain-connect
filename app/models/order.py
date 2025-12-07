from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    produce_id = Column(Integer, ForeignKey("produce.id"), nullable=False)

    quantity = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    status = Column(String, nullable=False, default="PENDING")
    # PENDING, ACCEPTED, REJECTED, DISPATCHED, COMPLETED, CANCELLED

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    vendor = relationship("Vendor")
    farmer = relationship("Farmer")
    produce = relationship("Produce")
