class FlashDealService:

    @staticmethod
    async def get_flash_deals(db):
        return [
            {
                "title": "50% OFF",
                "description": "Limited time flash deal"
            }
        ]
