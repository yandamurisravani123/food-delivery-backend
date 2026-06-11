from sqlalchemy import Column, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    food_id = Column(Integer, nullable=False)      # ✅ Fixed: menu_item_id -> food_id
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=True)     # ✅ added