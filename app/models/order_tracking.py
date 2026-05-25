# app/models/order_tracking.py

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey
)

from app.config.database import Base


class OrderTracking(Base):

    __tablename__ = "order_tracking"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    latitude = Column(
        Float,
        nullable=True
    )

    longitude = Column(
        Float,
        nullable=True
    )

    tracking_status = Column(
        String,
        default="preparing"
    )