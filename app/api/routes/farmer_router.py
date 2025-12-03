from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.farmer import FarmerCreate, FarmerResponse
from app.services.farmer_service import FarmerService

router = APIRouter(prefix="/farmers", tags=["farmers"])

@router.post("/", response_model=FarmerResponse)
def create_farmer(data: FarmerCreate, db: Session = Depends(get_db)):
    return FarmerService.create_farmer(db, data)

@router.get("/", response_model=list[FarmerResponse])
def list_farmers(db: Session = Depends(get_db)):
    return FarmerService.list_farmers(db)

@router.get("/{farmer_id}", response_model=FarmerResponse)
def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    return FarmerService.get_farmer(db, farmer_id)
