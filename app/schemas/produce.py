from pydantic import BaseModel, Field
from datetime import datetime

class ProducePublicResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: float
    farmer_id: int
    farmer_name: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            price=obj.price,
            quantity=obj.quantity,
            farmer_id=obj.farmer_id,
            created_at=obj.created_at,
            farmer_name=obj.farmer.name if hasattr(obj, "farmer") and obj.farmer else None
        )

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
