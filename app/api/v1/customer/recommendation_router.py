from fastapi import APIRouter

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)


@router.get("/")
async def recommend():
    return {"recommendations": []}
