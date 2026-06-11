<<<<<<< HEAD
from uuid import uuid4

from sqlalchemy import (
    Integer,
=======
import uuid

from sqlalchemy import (
    Column,
>>>>>>> 2f6cbfeb697fc8df4b0e6dc03fde77b955d4c69c
    String,
    Boolean,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

<<<<<<< HEAD
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
=======
from app.config.database import Base


class DeliveryNotification(Base):
>>>>>>> 2f6cbfeb697fc8df4b0e6dc03fde77b955d4c69c

from app.config.database import Base


class DeliveryNotification(Base):
    __tablename__ = "delivery_notification"

    notification_id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
<<<<<<< HEAD
        default=uuid4
=======
        default=uuid.uuid4
>>>>>>> 2f6cbfeb697fc8df4b0e6dc03fde77b955d4c69c
    )

    user_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    order_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False
    )

    title = mapped_column(
        String,
        nullable=False
    )

    message = mapped_column(
        String,
        nullable=False
    )

    notification_type = mapped_column(
        String,
        default="delivery_update"
    )

    is_read = mapped_column(
        Boolean,
        default=False
    )