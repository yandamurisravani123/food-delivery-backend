import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey,
    Date,
    Time,
    Boolean
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class Checkout(Base):

    __tablename__ = "checkout"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    address = Column(String(500), nullable=False)

    delivery_date = Column(Date, nullable=False)

    delivery_time = Column(Time, nullable=False)

    payment_method = Column(String(100), nullable=False)

    subtotal = Column(Float, nullable=False)

    delivery_fee = Column(Float, nullable=False)

    total = Column(Float, nullable=False)

    is_paid = Column(Boolean, default=False)
    
    user = relationship("User")