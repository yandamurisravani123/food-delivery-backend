import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    func
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id"),
        nullable=False,
    )

    coupon_code = Column(
        String,
        unique=True,
        nullable=False,
    )

    discount_type = Column(
        String,
        nullable=False,
    )

    discount_value = Column(
        Float,
        nullable=False,
    )

    max_discount_cap = Column(Float)

    minimum_order_value = Column(
        Float,
        default=0,
    )

    total_usage_limit = Column(
        Integer,
        default=1,
    )

    current_usage_count = Column(
        Integer,
        default=0,
    )

    limit_per_customer = Column(
        Integer,
        default=1,
    )

    start_date = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    end_date = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    restaurant = relationship("Restaurant")