import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from app.config.database import Base


class InvoiceItem(Base):

    __tablename__ = "invoice_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    invoice_id = Column(
        UUID(as_uuid=True),
        ForeignKey("invoices.id"),
        nullable=False
    )

    item_name = Column(
        String(255),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    total = Column(
        Float,
        nullable=False
    )

    invoice = relationship("Invoice")