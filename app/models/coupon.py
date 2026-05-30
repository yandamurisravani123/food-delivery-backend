import uuid
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
<<<<<<< HEAD

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

=======
 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
 
from app.config.database import Base
 
 
class Coupon(Base):
    __tablename__ = "coupons"
 
>>>>>>> 6da5f03 (testing)
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id"),
        nullable=False,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    coupon_code = Column(
        String,
        unique=True,
        nullable=False,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    discount_type = Column(
        String,
        nullable=False,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    discount_value = Column(
        Float,
        nullable=False,
    )
<<<<<<< HEAD

    max_discount_cap = Column(Float)

=======
 
    max_discount_cap = Column(Float)
 
>>>>>>> 6da5f03 (testing)
    minimum_order_value = Column(
        Float,
        default=0,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    total_usage_limit = Column(
        Integer,
        default=1,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    current_usage_count = Column(
        Integer,
        default=0,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    limit_per_customer = Column(
        Integer,
        default=1,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    start_date = Column(
        DateTime(timezone=True),
        nullable=False,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    end_date = Column(
        DateTime(timezone=True),
        nullable=False,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    is_active = Column(
        Boolean,
        default=True,
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
<<<<<<< HEAD

    restaurant = relationship("Restaurant")
=======
 
    restaurant = relationship("Restaurant")
 
>>>>>>> 6da5f03 (testing)
