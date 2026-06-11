from fastapi import APIRouter

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

@router.get("/")
async def test():
    return {"message": "Payment router working"}