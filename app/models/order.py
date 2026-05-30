from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
from sqlalchemy.orm import mapped_column
from uuid import uuid4
class Order(Base):

    __tablename__ = "orders"

    order_id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid4
)

    user_id = Column(UUID(as_uuid=True), nullable=False)

    food_name = Column(String)

    cuisine = Column(String)

    order_time = Column(String)