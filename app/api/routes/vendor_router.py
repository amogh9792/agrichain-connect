from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.vendor import VendorCreate, VendorResponse
from app.services.vendor_service import VendorService

router = APIRouter(prefix="/vendors", tags=["Vendors"])

@router.post("/", response_model = VendorResponse)
def create_vendor(data: VendorCreate, db: Session = Depends(get_db)):
    return VendorService.create_vendor(db, data)

@router.get("/", response_model=list[VendorResponse])
def list_vendors(db: Session = Depends(get_db)):
    return VendorService.list_vendors(db)

@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    return VendorService.get_vendor(db, vendor_id)