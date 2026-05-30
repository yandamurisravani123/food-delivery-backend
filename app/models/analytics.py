from sqlalchemy import Column, Integer, Float, ForeignKey
<<<<<<< HEAD

from config.database import Base


class CampaignAnalytics(Base):
    __tablename__ = "campaign_analytics"

    id = Column(Integer, primary_key=True, index=True)

    campaign_id = Column(Integer, ForeignKey("campaigns.id"))

    impressions = Column(Integer, default=0)

    clicks = Column(Integer, default=0)

    orders = Column(Integer, default=0)

=======
 
from config.database import Base
 
 
class CampaignAnalytics(Base):
    __tablename__ = "campaign_analytics"
 
    id = Column(Integer, primary_key=True, index=True)
 
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
 
    impressions = Column(Integer, default=0)
 
    clicks = Column(Integer, default=0)
 
    orders = Column(Integer, default=0)
 
>>>>>>> 6da5f03 (testing)
    revenue = Column(Float, default=0)