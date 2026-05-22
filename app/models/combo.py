from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
import uuid


class MealCombo(Base):

    __tablename__ = "meal_combos"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id")
    )

    combo_name = Column(String(255), nullable=False)

    description = Column(String(1000), nullable=True)

    combo_price = Column(Float, nullable=False)

    tags = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)

    image_url = Column(String(255), nullable=True)