import uuid

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False
    )

    menu_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("menu_items.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        default=1
    )

    price = Column(
        Float,
        nullable=False
    )

    customer = relationship(
        "Customer"
    )

    menu_item = relationship(
        "MenuItem"
    )