from sqlalchemy.orm import Session
from app.models.order_tracking import OrderTracking
 
 
class TrackingService:
 
    @staticmethod
    def update_tracking(db: Session, data):
 
        tracking = OrderTracking(
            order_id=data.order_id,
            delivery_partner_id=data.delivery_partner_id,
            status=data.status,
            latitude=data.latitude,
            longitude=data.longitude,
            estimated_time=data.estimated_time
        )
 
        db.add(tracking)
        db.commit()
        db.refresh(tracking)
 
        return tracking
 
 