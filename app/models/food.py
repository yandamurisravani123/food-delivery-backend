from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean
)

from app.config.database import Base


class Food(Base):

    __tablename__ = "foods"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    image = Column(String)

    description = Column(String)

    category = Column(String)

    cuisine = Column(String)

    rating = Column(Float)

    preparation_time = Column(String)

    tags = Column(String)

    is_recommended = Column(Boolean, default=True)