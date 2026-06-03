import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime
)

from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class Search(Base):

    __tablename__ = "searches"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    keyword = Column(
        String(255),
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )