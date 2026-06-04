from fastapi import APIRouter

router = APIRouter(
    prefix="/savings",
    tags=["Savings"]
)


@router.get("/")
async def list_savings():
    return {"savings": []}
