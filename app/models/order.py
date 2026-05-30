from sqlalchemy import (
    Column,
    Float,
    Text,
    ForeignKey,
    DateTime,
    Integer,
    Boolean,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.config.database import Base
from sqlalchemy import Column, Integer

class Order(Base):

    __tablename__ = "orders"

    # PRIMARY KEY

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # FOREIGN KEYS

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id"),
        nullable=False
    )

    # =====================================================
    # ORDER DETAILS
    # =====================================================

    total_amount = Column(
        Float,
        default=0
    )

    status = Column(
        Text,
        default="pending"
    )

    payment_method = Column(
        Text,
        nullable=True
    )

    address = Column(
        Text,
        nullable=True
    )

    preparation_time = Column(
    Integer,
    nullable=True
    )

    # =====================================================
    # CUSTOMER ANALYTICS
    # =====================================================

    rating = Column(
        Float,
        nullable=True
    )

    review = Column(
        Text,
        nullable=True
    )

    visit_count = Column(
        Integer,
        default=1
    )

    # =====================================================
    # DASHBOARD ANALYTICS
    # =====================================================

    is_repeat = Column(
        Boolean,
        default=False
    )

    preparation_time = Column(
        Integer,
        nullable=True
    )

    delivery_time = Column(
        Integer,
        nullable=True
    )

    order_accuracy = Column(
        Float,
        default=100
    )

    customer_satisfaction = Column(
        Float,
        default=5.0
    )

    # =====================================================
    # BUSINESS METRICS
    # =====================================================

    marketing_source = Column(
        Text,
        nullable=True
    )

    campaign_name = Column(
        Text,
        nullable=True
    )

    waste_percentage = Column(
        Float,
        default=0
    )

    stock_used = Column(
        Float,
        default=0
    )

    # =====================================================
    # STAFF PERFORMANCE
    # =====================================================

    staff_rating = Column(
        Float,
        default=5.0
    )

    shift_type = Column(
        Text,
        nullable=True
    )

    # =====================================================
    # DATE & TIME
    # =====================================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    items = relationship(
        "OrderItems",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    user = relationship(
        "User",
        back_populates="orders"
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="orders"
    )

    # =====================================================
    # HELPER METHODS
    # =====================================================

    @property
    def is_completed(self):
        return self.status == "completed"

    @property
    def is_cancelled(self):
        return self.status == "cancelled"

    @property
    def is_delivered(self):
        return self.status == "delivered"