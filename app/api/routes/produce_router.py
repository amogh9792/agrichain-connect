from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.produce import ProduceCreate, ProduceUpdate, ProduceResponse
from app.services.produce_service import ProduceService

router = APIRouter(prefix="/produce", tags=["Produce"])


@router.post("/", response_model=ProduceResponse)
def create_produce(data: ProduceCreate, db: Session = Depends(get_db)):
    return ProduceService.create_produce(db, data)


@router.get("/", response_model=list[ProduceResponse])
def list_produce(db: Session = Depends(get_db)):
    return ProduceService.list_produce(db)


@router.get("/{produce_id}", response_model=ProduceResponse)
def get_produce(produce_id: int, db: Session = Depends(get_db)):
    return ProduceService.get_produce(db, produce_id)


@router.put("/{produce_id}", response_model=ProduceResponse)
def update_produce(produce_id: int, data: ProduceUpdate, db: Session = Depends(get_db)):
    return ProduceService.update_produce(db, produce_id, data)


@router.delete("/{produce_id}")
def delete_produce(produce_id: int, db: Session = Depends(get_db)):
    return ProduceService.delete_produce(db, produce_id)


@router.get("/farmer/{farmer_id}", response_model=list[ProduceResponse])
def list_by_farmer(farmer_id: int, db: Session = Depends(get_db)):
    return ProduceService.list_by_farmer(db, farmer_id)
