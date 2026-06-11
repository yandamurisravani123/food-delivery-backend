from sqlalchemy import UUID, Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey


class PreparationStep(Base):
    __tablename__ = "preparation_steps"

    id = Column(Integer, primary_key=True, index=True)


    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False
    )

    title = Column(String)
    status = Column(String, default="PENDING")  # PENDING | ACTIVE | DONE
    sequence = Column(Integer)

    timestamp = Column(DateTime, default=datetime.utcnow)