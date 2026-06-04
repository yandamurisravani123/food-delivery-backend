from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum, Boolean, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from datetime import datetime, timezone
from app.models.menu import MenuItem
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

    payment_method = Column(Text, nullable=True)
    address = Column(Text, nullable=True)

    rating = Column(Float, nullable=True)
    review = Column(Text, nullable=True)
    visit_count = Column(Integer, default=1)

    is_repeat = Column(Boolean, default=False)
    preparation_time = Column(Integer, nullable=True)
    delivery_time = Column(Integer, nullable=True)

    order_accuracy = Column(Float, default=100)
    customer_satisfaction = Column(Float, default=5.0)

    marketing_source = Column(Text, nullable=True)
    campaign_name = Column(Text, nullable=True)

    waste_percentage = Column(Float, default=0)
    stock_used = Column(Float, default=0)

    staff_rating = Column(Float, default=5.0)
    shift_type = Column(Text, nullable=True)

    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    
    user = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")

    
    @property
    def is_completed(self):
        return self.status == OrderStatus.completed

    @property
    def is_cancelled(self):
        return self.status == OrderStatus.cancelled