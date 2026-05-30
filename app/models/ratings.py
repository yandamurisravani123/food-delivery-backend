from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.config.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)

    # FIXED: INTEGER -> UUID
    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    driver_id = Column(
        Integer,
        ForeignKey("drivers.id"),
        nullable=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    rating = Column(Integer, nullable=False)
    feedback = Column(String, nullable=True)
    tag = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    customer = relationship("User")
    driver = relationship("Driver")
    order = relationship("Order")