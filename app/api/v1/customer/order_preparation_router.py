from fastapi import APIRouter

router = APIRouter(
    prefix="/order-preparation",
    tags=["Order Preparation"]
)


@router.get("/")
async def status():
    return {"message": "Order preparation placeholder"}
