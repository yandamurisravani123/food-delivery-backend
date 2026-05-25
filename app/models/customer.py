from fastapi import APIRouter

router = APIRouter()

@router.get("/customer")
def customer():
    return {"message": "Customer API"}