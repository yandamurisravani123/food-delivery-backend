from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
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

    menu_item_id = Column(UUID(as_uuid=True), ForeignKey("menu_items.id"))


    menu_item = relationship("MenuItem", back_populates="order_items")

    name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)

    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="items")