from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship

from app.config.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_name = Column(String, nullable=False)
    cuisine = Column(String, nullable=False)
    order_time = Column(String, nullable=False)

    user = relationship("User")