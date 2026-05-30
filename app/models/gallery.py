from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
import uuid


class FoodGallery(Base):

    __tablename__ = "food_gallery"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id")
    )

    menu_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("menu_items.id"),
        nullable=True
    )

    image_url = Column(String(500), nullable=False)

    status = Column(String(50), default="unassigned")