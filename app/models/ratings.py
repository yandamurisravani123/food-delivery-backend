from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
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
        default=datetime.utcnow
    )

    # Relationships
    customer = relationship("User")
    order = relationship("Order")

    # Only keep if Driver model exists
    driver = relationship("Driver")