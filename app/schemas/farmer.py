from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class FarmerCreate(BaseModel):
    name: str
    phone: str
    location: str | None = None

    @field_validator("phone")
    def validate_phone(cls, v):
        if not v:
            raise ValueError("Phone number is required")
        if not v.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(v) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return v


class FarmerResponse(BaseModel):
    id: int
    name: str
    phone: str
    location: str | None
    created_at: datetime

    class Config:
        from_attributes = True
