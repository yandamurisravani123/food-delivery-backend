from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.config.database import Base


class Banner(Base):

    __tablename__ = "banners"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    image = Column(String)