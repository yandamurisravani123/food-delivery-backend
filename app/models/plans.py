from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import JSON
 
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
 
from app.config.database import Base
 
 
class Plan(Base):
    __tablename__ = "plans"
 
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
 
    name = Column(
        String(100),
        nullable=False
    )
 
    price = Column(
        Float,
        nullable=False
    )
 
    description = Column(
        String(500),
        nullable=True
    )
 
    duration_days = Column(
        Integer,
        nullable=False
    )
 
    free_trial_days = Column(
        Integer,
        default=0
    )
 
    is_popular = Column(
        Boolean,
        default=False
    )
 
    # UI Badge
    # Example: MOST POPULAR, BEST VALUE
    badge_text = Column(
        String(100),
        nullable=True
    )
 
    # Button Text
    # Example: Continue with Basic
    # Example: Start Premium Trial
    button_text = Column(
        String(100),
        nullable=True
    )
 
    # UI Theme Color
    # Example: #F97316
    theme_color = Column(
        String(50),
        nullable=True
    )
 
    # Plan Icon URL
    icon_url = Column(
        String(500),
        nullable=True
    )
 
    # Featured Plan
    is_featured = Column(
        Boolean,
        default=False
    )
 
    # Active / Inactive Plan
    is_active = Column(
        Boolean,
        default=True
    )
 
    # Plan Display Order
    display_order = Column(
        Integer,
        default=0
    )
 
    # Extra Dynamic Settings
    metadata_json = Column(
        JSON,
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
 
    # Soft Delete
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )
 
    features = relationship(
        "Feature",
        back_populates="plan"
    )