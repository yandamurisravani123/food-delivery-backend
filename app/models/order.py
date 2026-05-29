from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    food_name = Column(String, nullable=False)
    cuisine = Column(String, nullable=False)
    order_time = Column(String, nullable=False)

    user = relationship(
        "User",
        back_populates="orders"
    )