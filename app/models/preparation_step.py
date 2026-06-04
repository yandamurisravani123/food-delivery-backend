from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.config.database import Base


class PreparationStep(Base):
    __tablename__ = "preparation_steps"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))

    title = Column(String)
    status = Column(String, default="PENDING")  # PENDING | ACTIVE | DONE
    sequence = Column(Integer)

    timestamp = Column(DateTime, default=datetime.utcnow)