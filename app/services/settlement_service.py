from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.models.settlement import Settlement
 
 
async def get_settlement_by_id(
    db: AsyncSession,
    settlement_id: str,
):
    query = select(Settlement).where(
        Settlement.settlement_id == settlement_id
    )
 
    result = await db.execute(query)
 
    return result.scalar_one_or_none()