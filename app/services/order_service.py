from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order
from app.models.vendor import Vendor
from app.models.farmer import Farmer
from app.models.produce import Produce
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.core.logging_config import logger

VALID_STATUSES = {"PENDING", "ACCEPTED", "REJECTED", "DISPATCHED", "COMPLETED", "CANCELLED"}


class OrderService:

    @staticmethod
    def create_order(db: Session, data: OrderCreate) -> Order:
        logger.info(
            f"Order create attempt | vendor_id={data.vendor_id}, "
            f"produce_id={data.produce_id}, quantity={data.quantity}"
        )

        vendor = db.query(Vendor).filter(Vendor.id == data.vendor_id).first()
        if not vendor:
            logger.warning(f"Order create failed | vendor not found id={data.vendor_id}")
            raise HTTPException(status_code=400, detail="Vendor does not exist")

        produce = db.query(Produce).filter(Produce.id == data.produce_id).first()
        if not produce:
            logger.warning(f"Order create failed | produce not found id={data.produce_id}")
            raise HTTPException(status_code=400, detail="Produce does not exist")

        farmer = db.query(Farmer).filter(Farmer.id == produce.farmer_id).first()
        if not farmer:
            logger.error(
                f"Order create failed | farmer missing for produce_id={data.produce_id}, "
                f"farmer_id={produce.farmer_id}"
            )
            raise HTTPException(status_code=500, detail="Farmer mapping error for produce")

        total_price = data.quantity * produce.price

        order = Order(
            vendor_id=data.vendor_id,
            farmer_id=produce.farmer_id,
            produce_id=data.produce_id,
            quantity=data.quantity,
            total_price=total_price,
            status="PENDING",
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        logger.info(f"Order created | order_id={order.id}, total_price={order.total_price}")
        return order

    @staticmethod
    def get_order(db: Session, order_id: int) -> Order:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            logger.warning(f"Order fetch failed | id={order_id}")
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    @staticmethod
    def list_by_vendor(db: Session, vendor_id: int):
        logger.info(f"List orders by vendor | vendor_id={vendor_id}")
        return (
            db.query(Order)
            .filter(Order.vendor_id == vendor_id)
            .order_by(Order.id.desc())
            .all()
        )

    @staticmethod
    def list_by_farmer(db: Session, farmer_id: int):
        logger.info(f"List orders by farmer | farmer_id={farmer_id}")
        return (
            db.query(Order)
            .filter(Order.farmer_id == farmer_id)
            .order_by(Order.id.desc())
            .all()
        )

    @staticmethod
    def update_status(db: Session, order_id: int, data: OrderStatusUpdate) -> Order:
        logger.info(f"Order status update attempt | order_id={order_id}, new_status={data.status}")

        if data.status not in VALID_STATUSES:
            logger.warning(f"Order status update failed | invalid status={data.status}")
            raise HTTPException(status_code=400, detail="Invalid status")

        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            logger.warning(f"Order status update failed | order not found id={order_id}")
            raise HTTPException(status_code=404, detail="Order not found")

        order.status = data.status
        db.commit()
        db.refresh(order)

        logger.info(f"Order status updated | order_id={order.id}, status={order.status}")
        return order
