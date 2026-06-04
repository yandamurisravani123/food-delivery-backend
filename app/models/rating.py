from sqlalchemy import Column, Integer, Float, ForeignKey
from app.config.database import Base
 
 
class Rating(Base):
 
    __tablename__ = "ratings"
 
    id = Column(Integer, primary_key=True)
 
    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id")
    )
 
    rating = Column(Float)