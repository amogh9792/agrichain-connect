from pydantic import BaseModel, Field
from datetime import datetime

class ProduceBase(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    quantity: float = Field(..., gt=0)
    farmer_id: int

class ProduceCreate(ProduceBase):
    pass

class ProduceUpdate(BaseModel):
    name: str | None = None
    price: float | None = Field(None, gt=0)
    quantity: float | None = Field(None, gt=0)

class ProduceResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: float
    farmer_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
