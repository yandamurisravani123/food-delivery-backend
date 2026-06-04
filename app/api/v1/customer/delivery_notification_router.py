from fastapi import APIRouter

router = APIRouter(
    prefix="/delivery-notifications",
    tags=["Delivery Notifications"]
)


@router.get("/")
async def list_notifications():
    return {"notifications": []}
