from fastapi import APIRouter

router = APIRouter(
    prefix="/order-tracking",
    tags=["Order Tracking"]
)


@router.get("/")
async def status():
    return {"message": "Order tracking placeholder"}
