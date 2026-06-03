from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
 
from app.config.database import Base
 
 
class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
 
    user_id = Column(UUID(as_uuid=True), nullable=False)
 
    transaction_type = Column(String, nullable=False)
 
    amount = Column(Float, nullable=False)
 
    description = Column(String)
 
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
 