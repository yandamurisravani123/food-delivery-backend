from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
<<<<<<< HEAD
    Float
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class OrderItems(Base):

    __tablename__ = "order_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    menu_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("menu_items.id")
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    # RELATIONSHIPS
    order = relationship(
        "Order",
        back_populates="items"
    )

    menu_item = relationship(
        "MenuItem",
        back_populates="order_items"
    )
=======
    Float,
    String,
    String
)
 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
 
from app.config.database import Base
 
 
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)  # ✅ ADD THIS

    name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")
>>>>>>> 6da5f03 (testing)
