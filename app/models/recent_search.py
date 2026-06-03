from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.config.database import Base


class RecentSearch(Base):

    __tablename__ = "recent_searches"

    id = Column(Integer, primary_key=True)

    keyword = Column(String)