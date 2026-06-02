from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.sql import func
 
from sqlalchemy.orm import relationship
 
from app.config.database import Base
 
 
class Feature(Base):
    __tablename__ = "features"
 
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
 
    plan_id = Column(
        Integer,
        ForeignKey("plans.id"),
        nullable=False
    )
 
    feature_name = Column(
        String(255),
        nullable=False
    )
 
    included = Column(
        Boolean,
        default=True,
        nullable=False
    )
 
    # Display order for frontend
    display_order = Column(
        Integer,
        default=0
    )
 
    # Show/Hide feature
    is_active = Column(
        Boolean,
        default=True
    )
 
    # Optional icon
    icon_url = Column(
        String(500),
        nullable=True
    )
 
    # Optional short description
    description = Column(
        String(500),
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
 
    # Relationship
    plan = relationship(
        "Plan",
        back_populates="features"
    )