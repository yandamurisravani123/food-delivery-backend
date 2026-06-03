from pydantic import BaseModel
from typing import Optional
class FeatureCreate(BaseModel):
    plan_id: int
    feature_name: str
    included: bool = True
class FeatureResponse(BaseModel):
    id: int
    plan_id: int
    feature_name: str
    included: bool
    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import Optional
class FeatureCreate(BaseModel):
    plan_id: int
    feature_name: str
    included: bool = True
class FeatureResponse(BaseModel):
    id: int
    plan_id: int
    feature_name: str
    included: bool
    class Config:
        from_attributes = True