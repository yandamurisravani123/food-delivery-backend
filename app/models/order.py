from sqlalchemy import (
    Column,
    Integer,
    String,
    Float
)

from app.config.database import Base


   
class Order(Base):

    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    food_name = Column(
        String,
        nullable=False
    )

    cuisine = Column(String)

    order_time = Column(String)

   

    order_status = Column(
        String,
        default="placed"
    )
   

    estimated_time = Column(
        Integer,
        nullable=True
    )

    delivery_boy_name = Column(
        String,
        nullable=True
    )

    delivery_boy_phone = Column(
        String,
        nullable=True
    )

    delivery_rating = Column(
        Float,
        default=0.0
    )

    latitude = Column(
        Float,
        nullable=True
    )

    longitude = Column(
        Float,
        nullable=True
    )