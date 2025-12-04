from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate
from app.core.logging_config import logger

class VendorService:

    @staticmethod
    def create_vendor(db: Session, data: VendorCreate):
        logger.info(f"Vendor create attempt: phone = {data.phone}, name = {data.name}")

        existing = db.query(Vendor).filter(Vendor.phone == data.phone).first()
        if existing:
            logger.warning(f"Vendor creation Failed: Duplicate phone: {data.phone}")
            raise HTTPException(400, "Phone alread exists!")
        
        vendor = Vendor(**data.dict())
        db.add(vendor)
        db.commit()
        db.refresh(vendor)

        logger.info(f"Vendor created successfully: id = {vendor.id}, phone = {vendor.phone}")
        return vendor
    
    @staticmethod
    def list_vendors(db: Session):
        logger.info("Fetching all vendors")
        return db.query(Vendor).all()
    
    @staticmethod
    def get_vendor(db: Session, vendor_id: int):
        logger.info(f"Fetching vendor with id = {vendor_id}")

        vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
        if not vendor:
            logger.warning(f"Vendor not found: id = {vendor_id}")
            raise HTTPException(404, "Vendor not found")
        

        return vendor