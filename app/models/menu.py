<<<<<<< HEAD
from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
import uuid


class MenuItem(Base):

    __tablename__ = "menu_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id")
    )

    item_name = Column(String(255), nullable=False)

    description = Column(String(1000), nullable=True)

    category = Column(String(100), nullable=True)

    base_price = Column(Float, nullable=False)

    tags = Column(String(255), nullable=True)

    tax_rate = Column(String(50), nullable=True)

    track_stock = Column(Boolean, default=True)

    combo_available = Column(Boolean, default=False)

    image_url = Column(String(255), nullable=True)
    
    is_available = Column(Boolean, default=True)
    
    track_stock = Column(Boolean, default=True)
    
    tax_category = Column(String(100), nullable=True)
=======
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # ← UUID not Integer
    restaurant_id = Column(UUID(as_uuid=True), nullable=True)
    item_name = Column(String)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    base_price = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    tax_rate = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    track_stock = Column(Boolean, default=True)
    combo_available = Column(Boolean, default=False)
    image_url = Column(String, nullable=True)
    auto_disable = Column(Boolean, default=True)
    minimum_stock_required = Column(Integer, default=1)
    swiggy_synced = Column(Boolean, default=False)
    zomato_synced = Column(Boolean, default=False)
    last_synced_at = Column(DateTime, nullable=True)
>>>>>>> smart-bidding-feature
