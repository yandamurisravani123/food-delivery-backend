from sqlalchemy import Column, Integer, Float, ForeignKey
from app.config.database import Base
<<<<<<< HEAD


class Rating(Base):

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)

=======
 
 
class Rating(Base):
 
    __tablename__ = "ratings"
 
    id = Column(Integer, primary_key=True)
 
>>>>>>> 6da5f03 (testing)
    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id")
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    rating = Column(Float)