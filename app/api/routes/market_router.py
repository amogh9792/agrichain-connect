from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.produce import ProducePublicResponse
from app.services.market_service import MarketService

router = APIRouter(prefix="/market", tags=["Market"])

@router.get("/produce", response_model=dict)
def list_market_produce(
    name: str | None = Query(None),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    farmer_id: int | None = Query(None),
    sort: str | None = Query(None, regex="^(price_low_to_high|price_high_to_low)$"),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    items, total = MarketService.list_produce(db, name, min_price, max_price, farmer_id, sort, limit, offset)
    results = [ProducePublicResponse.from_orm(i) for i in items]
    return {"total": total, "limit": limit, "offset": offset, "results": results}


@router.get("/produce/{produce_id}", response_model=ProducePublicResponse)
def get_market_produce(produce_id: int, db: Session = Depends(get_db)):
    item = MarketService.get_market_produce(db, produce_id)
    if not item:
        raise HTTPException(404, "Produce not found")
    return ProducePublicResponse.from_orm(item)
