from sqlalchemy import (
    Column,
    Integer,
    String
)

from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class UserPreference(Base):

    __tablename__ = "user_preferences"

    id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4
    )

    user_id = Column(UUID(as_uuid=True))

    favorite_cuisine = Column(String)

    spicy_level = Column(String)

    preferred_food_type = Column(String)