# models/food_image.py

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.config.database import Base


class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), nullable=False)

    image_url = Column(String, nullable=False)

    menu_item_id = Column(UUID(as_uuid=True), ForeignKey("menu_items.id"), nullable=True)

    is_assigned = Column(Boolean, default=False)