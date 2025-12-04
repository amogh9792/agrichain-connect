from pydantic import BaseModel, Field

class VendorCreate(BaseModel):
    name: str
    phone: str = Field(..., min_length=10, max_length=10)
    company_name: str | None = None
    location: str | None = None

class VendorResponse(BaseModel):
    id: int
    name: str
    phone: str
    company_name: str | None
    location: str | None

    class config:
        from_attributes = True