from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.subscription_service import SubscriptionService
router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])
@router.post("/subscribe/{plan_id}")
def subscribe(plan_id: int, db: Session = Depends(get_db)):
    return SubscriptionService.subscribe(db, plan_id)
@router.get("/current")
def current_subscription(db: Session = Depends(get_db)):
    return SubscriptionService.get_current_subscription(db)
@router.get("/history")
def subscription_history(db: Session = Depends(get_db)):
    return SubscriptionService.get_subscription_history(db)
@router.delete("/{subscription_id}")
def cancel_subscription(subscription_id: int, db: Session = Depends(get_db)):
    return SubscriptionService.cancel_subscription(db, subscription_id)
 