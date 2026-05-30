from datetime import datetime
from datetime import timedelta
 
from sqlalchemy.orm import Session
 
from app.models.plan import Plan
from app.models.subscription import Subscription
 
 
class SubscriptionService:
 
    @staticmethod
    def subscribe(
        db: Session,
        plan_id: int
    ):
 
        plan = (
            db.query(Plan)
            .filter(
                Plan.id == plan_id
            )
            .first()
        )
 
        if not plan:
            return None
 
        start_date = datetime.utcnow()
 
        end_date = (
            start_date +
            timedelta(
                days=plan.duration_days
            )
        )
 
        subscription = Subscription(
            selected_plan=plan.name,
            start_date=start_date,
            end_date=end_date,
            status="ACTIVE"
        )
 
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
 
        return subscription
 
    @staticmethod
    def get_current_subscription(
        db: Session
    ):
        return (
            db.query(Subscription)
            .order_by(
                Subscription.id.desc()
            )
            .first()
        )
 
    @staticmethod
    def cancel_subscription(
        db: Session,
        subscription_id: int
    ):
 
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.id ==
                subscription_id
            )
            .first()
        )
 
        if not subscription:
            return None
 
        subscription.status = "CANCELLED"
 
        db.commit()
        db.refresh(subscription)
 
        return subscription
 
    @staticmethod
    def get_subscription_history(
        db: Session
    ):
        return (
            db.query(Subscription)
            .order_by(
                Subscription.id.desc()
            )
            .all()
        )