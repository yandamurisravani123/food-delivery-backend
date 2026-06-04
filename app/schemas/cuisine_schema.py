from pydantic import BaseModel


class CuisineResponse(BaseModel):

    id: int

    name: str

    image: str

    class Config:

        from_attributes = True