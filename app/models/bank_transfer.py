from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
 
from sqlalchemy.sql import func
 
from app.models.base import Base
 
 
class BankTransfer(Base):
 
    __tablename__ = "bank_transfers"
 
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
 
    transfer_reference = Column(
        String,
        unique=True,
        nullable=False
    )
 
    amount = Column(
        Float,
        default=0
    )
 
    transfer_status = Column(
        String,
        default="completed"
    )
 
    transfer_date = Column(
        String,
        nullable=False
    )
 
    transfer_time = Column(
        String,
        nullable=False
    )
 
    bank_name = Column(
        String,
        nullable=False
    )
 
    account_number = Column(
        String,
        nullable=False
    )
 
    routing_number = Column(
        String,
        nullable=False
    )
 
    account_type = Column(
        String,
        default="Business Checking"
    )
 
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
 