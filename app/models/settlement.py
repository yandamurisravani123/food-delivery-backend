# from sqlalchemy import Column
# from sqlalchemy import Integer
# from sqlalchemy import String
# from sqlalchemy import Float
# from sqlalchemy import DateTime

# from sqlalchemy.sql import func
# from sqlalchemy.orm import Mapped, mapped_column
# from datetime import datetime

# from app.models.base import Base


# class Settlement(Base):

#     __tablename__ = "settlements"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True
#     )

#     settlement_id = Column(
#         String,
#         unique=True,
#         nullable=False
#     )

#     cycle = Column(
#         String,
#         nullable=False
#     )

#     gross_sales = Column(
#         Float,
#         default=0
#     )

#     deductions = Column(
#         Float,
#         default=0
#     )

#     net_payout = Column(
#         Float,
#         default=0
#     )
    
#     platform_fees = Column(
#         Float,
#         default=0
#     )

#     # ADD THIS
#     discounts = Column(
#         Float,
#         default=0
#     )

#     # ADD THIS
#     tax_adjustment = Column(
#         Float,
#         default=0
#     )

#     # ADD THIS
#     merchant_share_percentage = Column(
#         Float,
#         default=82
#     )
    
#     # ADD THIS
#     platform_fee_percentage = Column(
#         Float,
#         default=14
#     )

#     # ADD THIS
#     discount_percentage = Column(
#         Float,
#         default=4
#     )

#     status = Column(
#         String,
#         default="processed"
#     )

#     created_at = Column(
#         DateTime(timezone=True),
#         server_default=func.now()
#     )


from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from app.models.base import Base


class Settlement(Base):

    __tablename__ = "settlements"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    settlement_id = Column(
        String,
        unique=True,
        nullable=False
    )

    cycle = Column(
        String,
        nullable=False
    )

    gross_sales = Column(
        Float,
        default=0
    )

    deductions = Column(
        Float,
        default=0
    )

    net_payout = Column(
        Float,
        default=0
    )

    platform_fees = Column(
        Float,
        default=0
    )

    discounts = Column(
        Float,
        default=0
    )

    tax_adjustment = Column(
        Float,
        default=0
    )

    merchant_share_percentage = Column(
        Float,
        default=82
    )

    platform_fee_percentage = Column(
        Float,
        default=14
    )

    discount_percentage = Column(
        Float,
        default=4
    )

    # NEW
    merchant_share = Column(
        Float,
        default=0
    )

    # NEW
    delivery_commission = Column(
        Float,
        default=0
    )

    # NEW
    payment_gateway_fee = Column(
        Float,
        default=0
    )

    # NEW
    total_orders = Column(
        Integer,
        default=0
    )

    status = Column(
        String,
        default="processed"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
