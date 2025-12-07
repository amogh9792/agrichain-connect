from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

OrderStatus = Literal["PENDING", "ACCEPTED", "REJECTED", "DISPATCHED", "COMPLETED", "CANCELLED"]


class OrderCreate(BaseModel):
    vendor_id: int
    produce_id: int
    quantity: float = Field(..., gt=0)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderResponse(BaseModel):
    id: int
    vendor_id: int
    farmer_id: int
    produce_id: int
    quantity: float
    total_price: float
    status: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
