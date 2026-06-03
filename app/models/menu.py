import uuid

from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.config.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=True)
    item_name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    category = Column(String(100), nullable=True)
    base_price = Column(Float, nullable=False)
    tags = Column(String(255), nullable=True)
    tax_rate = Column(String(50), nullable=True)
    tax_category = Column(String(100), nullable=True)
    is_available = Column(Boolean, default=True)
    track_stock = Column(Boolean, default=True)
    combo_available = Column(Boolean, default=False)
    image_url = Column(String(255), nullable=True)
    auto_disable = Column(Boolean, default=True)
    minimum_stock_required = Column(Integer, default=1)
    swiggy_synced = Column(Boolean, default=False)
    zomato_synced = Column(Boolean, default=False)
    last_synced_at = Column(DateTime, nullable=True)

    order_items = relationship("OrderItems", back_populates="menu_item")
