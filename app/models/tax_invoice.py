from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
 
from sqlalchemy.sql import func
 
from app.models.base import Base
 
 
class TaxInvoice(Base):
 
    __tablename__ = "tax_invoices"
 
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
 
    invoice_id = Column(
        String,
        unique=True,
        nullable=False
    )
 
    month = Column(
        String,
        nullable=False
    )
 
    invoice_type = Column(
        String,
        nullable=False
    )
 
    gst_amount = Column(
        Float,
        default=0
    )
 
    tds_amount = Column(
        Float,
        default=0
    )
 
    total_amount = Column(
        Float,
        default=0
    )
 
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
 