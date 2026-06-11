from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.config.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        nullable=False,  # ✅ Fixed: added missing comma
        unique=True
    )

    favorite_cuisine = Column(String, nullable=True)
    spicy_level = Column(String, nullable=True)
    preferred_food_type = Column(String, nullable=True)