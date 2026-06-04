from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.models.settlement import Settlement
 
 
async def get_all_settlements(
    db: AsyncSession,
    search: str = None
):
 
    query = select(Settlement)
 
    if search:
 
        query = query.where(
            Settlement.settlement_id.ilike(
                f"%{search}%"
            )
        )
 
    result = await db.execute(query)
 
    return result.scalars().all()
 