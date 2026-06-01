from app.models.checkout import Checkout
 
 
class CheckoutRepository:
 
    @staticmethod
    async def create_checkout(db, data):
 
        checkout = Checkout(**data)
 
        db.add(checkout)
 
        await db.commit()
 
        await db.refresh(checkout)
 
        return checkout
 