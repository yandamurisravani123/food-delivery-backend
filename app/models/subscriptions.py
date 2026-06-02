from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
 
from sqlalchemy.sql import func
 
from app.config.database import Base
 
 
class Subscription(Base):
    __tablename__ = "subscriptions"
 
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
 
    selected_plan = Column(
        String(100),
        nullable=False
    )
 
    status = Column(
        String(50),
        nullable=False,
        default="ACTIVE"
    )
 
    # Free Trial Tracking
    trial_used = Column(
        Boolean,
        default=False
    )
 
    trial_start_date = Column(
        DateTime(timezone=True),
        nullable=True
    )
 
    trial_end_date = Column(
        DateTime(timezone=True),
        nullable=True
    )
 
    # Subscription Dates
    start_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
 
    end_date = Column(
        DateTime(timezone=True),
        nullable=True
    )
 
    # Cancellation
    cancelled_at = Column(
        DateTime(timezone=True),
        nullable=True
    )
 
    # Audit Fields
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
 
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )