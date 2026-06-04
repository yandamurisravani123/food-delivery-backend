from fastapi import APIRouter

router = APIRouter(
    prefix="/customer/rewards",
    tags=["Rewards"]
)


@router.get("/")
async def get_rewards():
    return {
        "rewards": [],
        "message": "Rewards endpoint placeholder"
    }
