from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
from sqlalchemy.orm import mapped_column

class Order(Base):

    __tablename__ = "orders"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=UUID.UUID4,
        index=True,
    )

    user_id = Column(UUID(as_uuid=True), nullable=False)

    food_name = Column(String)

    cuisine = Column(String)

    order_time = Column(String)