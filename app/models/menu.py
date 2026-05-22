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