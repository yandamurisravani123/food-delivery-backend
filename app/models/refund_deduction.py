from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
 
from sqlalchemy.sql import func
 
from app.models.base import Base
 
 
class RefundDeduction(Base):
 
    __tablename__ = "refund_deductions"
 
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
 
    order_id = Column(
        String,
        nullable=False
    )
 
    category = Column(
        String,
        nullable=False
    )
 
    reason = Column(
        String,
        nullable=False
    )
 
    deduction_amount = Column(
        Float,
        default=0
    )
 
    refund_status = Column(
        String,
        default="active"
    )
 
    risk_level = Column(
        String,
        default="low"
    )
 
    created_at_label = Column(
        String,
        nullable=False
    )
 
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
 