from pydantic import BaseModel


class MenuResponse(BaseModel):

    id: int
    name: str
    price: float
    image: str

    class Config:
        from_attributes = True