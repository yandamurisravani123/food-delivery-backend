from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey,
    Integer, String, Text, func,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

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

    # Timestamps
    order_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    start_time = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Pricing
    subtotal = Column(Float, default=0)
    delivery_fee = Column(Float, default=0)
    tax_percent = Column(Float, default=8)
    total = Column(Float, default=0)

    # Status
    status = Column(SQLEnum(OrderStatus, name="orderstatus"), default=OrderStatus.pending)

    # Delivery
    courier_name = Column(String, nullable=True)
    courier_rating = Column(String, nullable=True)
    delivery_address = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    payment_method = Column(Text, nullable=True)

    # Order details
    prep_time = Column(Integer, default=0)
    is_urgent = Column(String, default="normal")
    special_instructions = Column(String, nullable=True)
    packaging_notes = Column(String, nullable=True)
    cutlery_required = Column(Boolean, default=True)
    extras = Column(String, nullable=True)

    # Customer analytics
    rating = Column(Float, nullable=True)
    review = Column(Text, nullable=True)
    visit_count = Column(Integer, default=1)

    # Dashboard analytics
    is_repeat = Column(Boolean, default=False)
    preparation_time = Column(Integer, nullable=True)
    delivery_time = Column(Integer, nullable=True)
    order_accuracy = Column(Float, default=100)
    customer_satisfaction = Column(Float, default=5.0)

    # Business metrics
    marketing_source = Column(Text, nullable=True)
    campaign_name = Column(Text, nullable=True)
    waste_percentage = Column(Float, default=0)
    stock_used = Column(Float, default=0)

    # Staff performance
    staff_rating = Column(Float, default=5.0)
    shift_type = Column(Text, nullable=True)

    # Relationships — single definition referencing the correct class name
    items = relationship("OrderItems", back_populates="order", cascade="all, delete-orphan")
    user = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")

    # Helper properties
    @property
    def is_completed(self):
        return self.status == OrderStatus.completed

    @property
    def is_cancelled(self):
        return self.status == OrderStatus.cancelled

    @property
    def is_delivered(self):
        return self.status == OrderStatus.completed