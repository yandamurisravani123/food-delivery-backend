from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.config.database import Base


class UserLocation(Base):

    __tablename__ = "user_locations"

    id = Column(Integer, primary_key=True)

    city = Column(String)

    state = Column(String)