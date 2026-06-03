from sqlalchemy import (
    Column,
    Integer,
    Float,
    Text,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.config.database import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(UUID(as_uuid=True), nullable=False)

    order_id = Column(Integer, nullable=False)

    rating = Column(Float, nullable=False)

    review = Column(Text)

    reward_points = Column(Integer, default=15)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )