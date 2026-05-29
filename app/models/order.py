from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from datetime import datetime, timezone

from app.config.database import Base


class OrderStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    preparing = "preparing"
    ready = "ready"
    packed = "packed"
    completed = "completed"
    cancelled = "cancelled"

class UrgencyLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
 
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=False)

   
    order_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    start_time = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    
    subtotal = Column(Float, default=0)
    delivery_fee = Column(Float, default=0)
    tax_percent = Column(Float, default=8)
    total = Column(Float, default=0)

    status = Column(
    SQLEnum(OrderStatus, name="orderstatus"),  
    default=OrderStatus.pending
)
    courier_name = Column(String, nullable=True)
    courier_rating = Column(String, nullable=True)
    delivery_address = Column(String, nullable=True)

   
    prep_time = Column(Integer, default=0)
    is_urgent = Column(String, default="normal")

    
    special_instructions = Column(String, nullable=True)
    extras = Column(String, nullable=True)
    packaging_notes = Column(String, nullable=True)
    cutlery_required = Column(Boolean, default=True)
    
    
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")