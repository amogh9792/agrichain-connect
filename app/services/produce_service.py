from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.produce import Produce
from app.models.farmer import Farmer
from app.schemas.produce import ProduceCreate, ProduceUpdate
from app.core.logging_config import logger


class ProduceService:

    @staticmethod
    def create_produce(db: Session, data: ProduceCreate):
        logger.info(f"Create produce attempt | farmer_id={data.farmer_id}, name={data.name}")

        farmer = db.query(Farmer).filter(Farmer.id == data.farmer_id).first()
        if not farmer:
            logger.warning(f"Creation failed | Farmer not found id={data.farmer_id}")
            raise HTTPException(status_code=400, detail="Farmer does not exist")

        produce = Produce(**data.dict())
        db.add(produce)
        db.commit()
        db.refresh(produce)

        logger.info(f"Produce created | id={produce.id}")
        return produce

    @staticmethod
    def list_produce(db: Session):
        logger.info("Fetch produce list")
        return db.query(Produce).all()

    @staticmethod
    def get_produce(db: Session, produce_id: int):
        produce = db.query(Produce).filter(Produce.id == produce_id).first()
        if not produce:
            logger.warning(f"Fetch failed | produce_id={produce_id}")
            raise HTTPException(status_code=404, detail="Produce not found")

        return produce

    @staticmethod
    def update_produce(db: Session, produce_id: int, data: ProduceUpdate):
        produce = db.query(Produce).filter(Produce.id == produce_id).first()
        if not produce:
            logger.warning(f"Update failed | id={produce_id}")
            raise HTTPException(status_code=404, detail="Produce not found")

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(produce, key, value)

        db.commit()
        db.refresh(produce)

        logger.info(f"Produce updated | id={produce_id}")
        return produce

    @staticmethod
    def delete_produce(db: Session, produce_id: int):
        produce = db.query(Produce).filter(Produce.id == produce_id).first()
        if not produce:
            logger.warning(f"Delete failed | id={produce_id}")
            raise HTTPException(status_code=404, detail="Produce not found")

        db.delete(produce)
        db.commit()
        logger.info(f"Produce deleted | id={produce_id}")

        return {"message": "Produce deleted"}

    @staticmethod
    def list_by_farmer(db: Session, farmer_id: int):
        logger.info(f"List produce for farmer_id={farmer_id}")
        return db.query(Produce).filter(Produce.farmer_id == farmer_id).all()
