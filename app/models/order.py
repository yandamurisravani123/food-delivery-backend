import uuid
from enum import Enum

from sqlalchemy import UUID, Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, func
from sqlalchemy.orm import mapped_column, relationship

from app.config.database import Base


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    restaurant_id = mapped_column(UUID(as_uuid=True), nullable=True, index=True)

    food_name = Column(String(255), nullable=True)
    cuisine = Column(String(100), nullable=True)

    status = Column(String(50), nullable=False, default=OrderStatus.pending.value)
    order_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    start_time = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    prep_time = Column(Integer, nullable=False, default=0)
    is_urgent = Column(Boolean, nullable=False, default=False)

    delivery_address = Column(Text, nullable=True)
    courier_name = Column(String(255), nullable=True)
    courier_rating = Column(String(50), nullable=True)
    special_instructions = Column(Text, nullable=True)
    packaging_notes = Column(Text, nullable=True)
    cutlery_required = Column(Boolean, nullable=False, default=True)

    subtotal = Column(Float, nullable=False, default=0.0)
    delivery_fee = Column(Float, nullable=False, default=0.0)
    tax_percent = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "orders_items"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id = mapped_column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False, default=0.0)

    order = relationship("Order", back_populates="items")