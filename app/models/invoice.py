import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey,
    DateTime,
    
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.config.database import Base


class Invoice(Base):

    __tablename__ = "invoices"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    order_id = Column(
    UUID(as_uuid=True),
    ForeignKey("orders.id"),
    nullable=False
    )

    invoice_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    restaurant_name = Column(
        String(255),
        nullable=False
    )

    restaurant_gstin = Column(
        String(100),
        nullable=False
    )

    customer_gstin = Column(
        String(100),
        nullable=True
    )

    subtotal = Column(Float, nullable=False)

    delivery_fee = Column(Float, nullable=False)

    gst = Column(Float, nullable=False)

    sgst = Column(Float, nullable=False)

    total_amount = Column(Float, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    order = relationship("Order")