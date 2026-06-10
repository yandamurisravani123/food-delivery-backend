from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
<<<<<<< HEAD

from app.config.database import Base  # ✅ Fixed: app.models.base -> app.config.database


=======
from sqlalchemy import Column, Integer

from app.models.base import Base
 
 
>>>>>>> 81a7d48d016c94dcee7c2e99ad3bb275aa433dca
class Refund(Base):
    __tablename__ = "refunds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
<<<<<<< HEAD
    order_id = Column(UUID(as_uuid=True), nullable=False)
=======
 
    order_id = Column(Integer, nullable=False)
 
>>>>>>> 81a7d48d016c94dcee7c2e99ad3bb275aa433dca
    user_id = Column(UUID(as_uuid=True), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="Initiated")
    created_at = Column(DateTime(timezone=True), server_default=func.now())