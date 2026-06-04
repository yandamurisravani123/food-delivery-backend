import uuid

from sqlalchemy import (
    Column,
    String,
    Float
)

from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class Map(Base):

    __tablename__ = "maps"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    restaurant_name = Column(
        String(255),
        nullable=False
    )

    latitude = Column(
        Float,
        nullable=False
    )

    longitude = Column(
        Float,
        nullable=False
    )

    address = Column(
        String(500),
        nullable=True
    )