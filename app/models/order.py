from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.config.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    food_name = Column(String)

    cuisine = Column(String)

    order_time = Column(String)