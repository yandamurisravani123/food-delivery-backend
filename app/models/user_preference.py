from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.config.database import Base


class UserPreference(Base):

    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    favorite_cuisine = Column(String)

    spicy_level = Column(String)

    preferred_food_type = Column(String)