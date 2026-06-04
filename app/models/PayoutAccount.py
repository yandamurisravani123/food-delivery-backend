import uuid
from sqlalchemy import Boolean, Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class PayoutAccount(Base):
    __tablename__ = "payout_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    driver_id = Column(
    UUID(as_uuid=True),
    ForeignKey("delivery_agents.id"),   
    nullable=False
  )
    account_holder_name = Column(String)
    account_number = Column(String)
    ifsc_code = Column(String)
    upi_id = Column(String, nullable=True)

    is_verified = Column(String, default="false")  
    
    is_verified = Column(Boolean, default=False)