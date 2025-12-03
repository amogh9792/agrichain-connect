from sqlalchemy.orm import Session
from app.models.farmer import Farmer
from app.schemas.farmer import FarmerCreate
from fastapi import HTTPException

class FarmerService:

    @staticmethod
    def create_farmer(db: Session, data: FarmerCreate):
        if db.query(Farmer).filter(Farmer.phone == data.phone).first():
            raise HTTPException(400, "Phone already registered")
        farmer = Farmer(**data.dict())
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
        return farmer

    @staticmethod
    def list_farmers(db: Session):
        return db.query(Farmer).all()

    @staticmethod
    def get_farmer(db: Session, farmer_id: int):
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            raise HTTPException(404, "Farmer not found")
        return farmer
