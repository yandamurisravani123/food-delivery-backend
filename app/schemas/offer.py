from pydantic import BaseModel


class OfferResponse(BaseModel):

    id: int
    title: str
    image: str
    description: str

    class Config:
        from_attributes = True