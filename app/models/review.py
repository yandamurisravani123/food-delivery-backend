
# app/models/review.py


import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base
from sqlalchemy import Column, Integer


class Review(Base):

    __tablename__ = "reviews"

    

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    
    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id"),
        nullable=False
    )

    
    order_id = Column(
        Integer,
        nullable=False
    )

    
    user_name = Column(
        String(100),
        nullable=False
    )

    
    comment = Column(
        String(500),
        nullable=True
    )

    
    rating = Column(
        Float,
        nullable=False
    )

    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )