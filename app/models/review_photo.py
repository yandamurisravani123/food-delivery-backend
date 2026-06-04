import uuid

from sqlalchemy import (
    Column,
    String,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class ReviewPhoto(Base):

    __tablename__ = "review_photos"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    review_id = Column(
        UUID(as_uuid=True),
        ForeignKey("reviews.id")
    )

    photo_url = Column(String)