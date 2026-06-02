from fastapi import APIRouter

router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)

@router.get("/tracking")
def tracking():
    return {"message": "Tracking API Working"}

@router.get("/notifications")
def get_notifications():
    return {
        "notifications": [
            {
                "title": "Order Confirmed",
                "message": "Your order has been confirmed"
            },
            {
                "title": "Out For Delivery",
                "message": "Delivery partner is on the way"
            }
        ]
    }