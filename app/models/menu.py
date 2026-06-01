import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class Menu(Base):

    __tablename__ = "menus"

    
    # Primary Key
    

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    
    # Restaurant Foreign Key
    
    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id"),
        nullable=False
    )

    
    # Menu Details
    

    name = Column(
        String(255),
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    image = Column(
        String(255),
        nullable=True
    )