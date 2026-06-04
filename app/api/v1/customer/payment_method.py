from fastapi import APIRouter

router = APIRouter(
    prefix="/payment-methods",
    tags=["Payment Methods"]
)


@router.get("/")
async def list_methods():
    return {"methods": []}
