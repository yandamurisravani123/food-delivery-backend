import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.config.database import Base

class MenuIngredient(Base):
    __tablename__ = "menu_ingredients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

menu_item_id = Column(UUID(as_uuid=True), ForeignKey("menu_items.id"))
ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id"))