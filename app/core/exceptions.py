from fastapi import HTTPException
 
 
class PlanNotFoundException(
    HTTPException
):
    def __init__(self):
 
        super().__init__(
            status_code=404,
            detail="Plan not found"
        )
 
 
class SubscriptionNotFoundException(
    HTTPException
):
    def __init__(self):
 
        super().__init__(
            status_code=404,
            detail="Subscription not found"
        )
 