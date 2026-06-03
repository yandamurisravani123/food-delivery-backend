from pydantic import BaseModel


class FlashDealResponse(BaseModel):

    id: int
    title: str
    image: str
    discount: str

    class Config:
        from_attributes = True
