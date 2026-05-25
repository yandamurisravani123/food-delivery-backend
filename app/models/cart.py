from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from app.config.database import Base


class Cart(Base):

    __tablename__ = "cart"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    food_id = Column(
        Integer,
        ForeignKey("foods.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        default=1
    )