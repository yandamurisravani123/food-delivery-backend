from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.config.database import Base
import uuid


class Cart(Base):
    __tablename__ = "cart"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    menu_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("menu_items.id"),   # FIXED
        nullable=False
    )

    quantity = Column(
        Integer,
        default=1
    )

    customer = relationship("Customer")
    menu_item = relationship("MenuItem")