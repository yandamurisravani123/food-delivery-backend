from pydantic import BaseModel


class RecentSearchResponse(BaseModel):

    id: int

    keyword: str

    class Config:

        from_attributes = True