

 
from sqlalchemy import Column, String, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
 
from app.config.database import Base
 
class Wallet(Base):
    __tablename__ = "wallets"
 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    balance = Column(Numeric, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 