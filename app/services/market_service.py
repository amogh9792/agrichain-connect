from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, asc, desc
from app.models.produce import Produce
from app.core.logging_config import logger

class MarketService:
    @staticmethod
    def _apply_filters(query, name, min_price, max_price, farmer_id):
        filters = []

        if name:
            filters.append(Produce.name.ilike(f"%{name}"))

        if min_price is not None:
            filters.append(Produce.price >= min_price)

        if max_price is not None:
            filters.append(Produce.price <= max_price)

        if farmer_id is not None:
            filters.append(Produce.farmer_id == farmer_id)
        
        if filters:
            query = query.filter(and_(*filters))
        
        return query
    

    @staticmethod
    def list_produce(
        db: Session,
        name: Optional[str],
        min_price: Optional[str],
        max_price: Optional[str],
        farmer_id: Optional[str],
        sort: Optional[str],
        limit: int,
        offset: int
    ) -> Tuple[List[Produce], int]:
        
        logger.info(f"Market Search | name = {name} | min = {min_price} | max = {max_price} "
                    f"| farmer = {farmer_id} | sort = {sort} | limit = {limit} | offset = {offset}")
        
        q = db.query(Produce)
        q = MarketService._apply_filters(q, name, min_price, max_price, farmer_id)

        total = q.count()

        if sort == "price_low_to_high":
            q = q.order_by(asc(Produce.price))

        elif sort == "price_high_to_low":
            q = q.order_by(desc(Produce.price))

        else:
            q = q.order_by(Produce.id.desc())

        results = q.offset(offset).limit(limit).all()

        logger.info(f"Market results: {len(results)} returned, total = {total}")
        return results, total
    
    @staticmethod
    def get_market_produce(db: Session, produce_id: int):
        item = db.query(Produce).filter(Produce.id == produce_id).first()
        if not item:
            logger.warning(f"Market fetch failed | id = {produce_id}")
            return None
        
        return item