class OfferService:

    @staticmethod
    async def get_offers(db):
        return [
            {
                "offer": "SAVE10",
                "discount": "10%"
            }
        ]
