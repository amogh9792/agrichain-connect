from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.logging_config import logger
from app.models.farmer import Farmer
from app.schemas.farmer import FarmerCreate


class FarmerService:

    @staticmethod
    def create_farmer(db: Session, data: FarmerCreate):
        logger.info(f"Farmer creation attempt: phone={data.phone}, name={data.name}")

        existing = db.query(Farmer).filter(Farmer.phone == data.phone).first()
        if existing:
            logger.warning(f"Farmer creation failed: duplicate phone={data.phone}")
            raise HTTPException(400, "Phone already registered")

        farmer = Farmer(**data.dict())
        db.add(farmer)
        db.commit()
        db.refresh(farmer)

        logger.info(f"Farmer created successfully: id={farmer.id}, phone={farmer.phone}")
        return farmer

    @staticmethod
    def list_farmers(db: Session):
        logger.info("Fetching all farmers")
        farmers = db.query(Farmer).all()
        logger.info(f"Fetched {len(farmers)} farmers")
        return farmers

    @staticmethod
    def get_farmer(db: Session, farmer_id: int):
        logger.info(f"Fetching farmer with id={farmer_id}")

        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            logger.warning(f"Farmer not found: id={farmer_id}")
            raise HTTPException(404, "Farmer not found")

        logger.info(f"Farmer found: id={farmer_id}, phone={farmer.phone}")
        return farmer
