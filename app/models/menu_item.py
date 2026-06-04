import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class MenuItem(Base):

    __tablename__ = "menu_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id"),
        nullable=False
    )

    item_name = Column(String(255), nullable=False)

    description = Column(Text, nullable=True)

    category = Column(String(100), nullable=True)

    base_price = Column(Float, nullable=False, default=0.0)

    tags = Column(String(255), nullable=True)

    tax_rate = Column(String(50), nullable=True)

    tax_category = Column(String(100), nullable=True)

    track_stock = Column(Boolean, default=True)

    combo_available = Column(Boolean, default=False)

    is_available = Column(Boolean, default=True)

    image_url = Column(String(500), nullable=True)
