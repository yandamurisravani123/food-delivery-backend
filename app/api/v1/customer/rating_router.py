from fastapi import APIRouter

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)


@router.get("/")
async def list_ratings():
    return {"ratings": []}
