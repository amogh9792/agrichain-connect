from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    return OrderService.create_order(db, data)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return OrderService.get_order(db, order_id)


@router.get("/vendor/{vendor_id}", response_model=list[OrderResponse])
def list_orders_by_vendor(vendor_id: int, db: Session = Depends(get_db)):
    return OrderService.list_by_vendor(db, vendor_id)


@router.get("/farmer/{farmer_id}", response_model=list[OrderResponse])
def list_orders_by_farmer(farmer_id: int, db: Session = Depends(get_db)):
    return OrderService.list_by_farmer(db, farmer_id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, data: OrderStatusUpdate, db: Session = Depends(get_db)):
    return OrderService.update_status(db, order_id, data)
