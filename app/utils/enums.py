import enum


class CampaignType(str, enum.Enum):
    DISCOUNT = "discount"
    FESTIVAL = "festival"
    SPONSORED = "sponsored"


class CampaignStatus(str, enum.Enum):
    ACTIVE = "active"
    SCHEDULED = "scheduled"
    PAUSED = "paused"
    COMPLETED = "completed"