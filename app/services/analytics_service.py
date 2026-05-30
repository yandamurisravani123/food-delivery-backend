from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from app.models.order_items import OrderItems
from app.models.menu import MenuItem


# =========================================================
# TOP SELLING BY QUANTITY
# =========================================================
async def get_top_selling_by_quantity(
    db: AsyncSession,
    restaurant_id
):

    query = (
        select(
            MenuItem.id,
            MenuItem.item_name,
            MenuItem.image_url,
            MenuItem.category,

            func.sum(
                OrderItems.quantity
            ).label("sold_units"),

            func.sum(
                OrderItems.quantity * OrderItems.price
            ).label("revenue")
        )

        .join(
            OrderItems,
            OrderItems.menu_item_id == MenuItem.id
        )

        .where(
            MenuItem.restaurant_id == restaurant_id
        )

        .group_by(
            MenuItem.id,
            MenuItem.item_name,
            MenuItem.image_url,
            MenuItem.category
        )

        .order_by(
            desc("sold_units")
        )
    )

    result = await db.execute(query)

    rows = result.all()

    return [
        {
            "item_id": str(row.id),

            "item_name": row.item_name,

            "image_url": row.image_url,

            "category": row.category,

            "sold_units": int(
                row.sold_units or 0
            ),

            "revenue": float(
                row.revenue or 0
            )
        }

        for row in rows
    ]


# =========================================================
# TOP SELLING BY REVENUE
# =========================================================
async def get_top_selling_by_revenue(
    db: AsyncSession,
    restaurant_id
):

    query = (
        select(
            MenuItem.id,
            MenuItem.item_name,
            MenuItem.image_url,
            MenuItem.category,

            func.sum(
                OrderItems.quantity
            ).label("sold_units"),

            func.sum(
                OrderItems.quantity * OrderItems.price
            ).label("revenue")
        )

        .join(
            OrderItems,
            OrderItems.menu_item_id == MenuItem.id
        )

        .where(
            MenuItem.restaurant_id == restaurant_id
        )

        .group_by(
            MenuItem.id,
            MenuItem.item_name,
            MenuItem.image_url,
            MenuItem.category
        )

        .order_by(
            desc("revenue")
        )
    )

    result = await db.execute(query)

    rows = result.all()

    return [
        {
            "item_id": str(row.id),

            "item_name": row.item_name,

            "image_url": row.image_url,

            "category": row.category,

            "sold_units": int(
                row.sold_units or 0
            ),

            "revenue": float(
                row.revenue or 0
            )
        }

        for row in rows
    ]


# =========================================================
# CATEGORY INSIGHTS
# =========================================================
async def get_category_insights(
    db: AsyncSession,
    restaurant_id
):

    query = (
        select(
            MenuItem.category,

            func.sum(
                OrderItems.quantity
            ).label("total_units")
        )

        .join(
            OrderItems,
            OrderItems.menu_item_id == MenuItem.id
        )

        .where(
            MenuItem.restaurant_id == restaurant_id
        )

        .group_by(
            MenuItem.category
        )
    )

    result = await db.execute(query)

    rows = result.all()

    total = sum(
        row.total_units for row in rows
    ) or 1

    return [

        {
            "category": row.category,

            "percentage": round(
                (row.total_units / total) * 100,
                2
            )
        }

        for row in rows
    ]


# =========================================================
# MENU RANKINGS
# =========================================================
async def get_menu_rankings(
    db: AsyncSession,
    restaurant_id
):

    query = (
        select(
            MenuItem.id,

            MenuItem.item_name,

            MenuItem.image_url,

            MenuItem.category,

            func.sum(
                OrderItems.quantity
            ).label("sold_units")
        )

        .join(
            OrderItems,
            OrderItems.menu_item_id == MenuItem.id
        )

        .where(
            MenuItem.restaurant_id == restaurant_id
        )

        .group_by(
            MenuItem.id,
            MenuItem.item_name,
            MenuItem.image_url,
            MenuItem.category
        )

        .order_by(
            desc("sold_units")
        )

        .offset(1)

        .limit(10)
    )

    result = await db.execute(query)

    rows = result.all()

    rankings = []

    for index, row in enumerate(rows, start=2):

        rankings.append({

            "rank": index,

            "item_id": str(row.id),

            "item_name": row.item_name,

            "image_url": row.image_url,

            "category": row.category,

            "sold_units": int(
                row.sold_units or 0
            )
        })

    return rankings


# =========================================================
# COMPLETE DASHBOARD
# =========================================================
async def get_dashboard_data(
    db: AsyncSession,
    restaurant_id
):

    top_items = await get_top_selling_by_quantity(
        db,
        restaurant_id
    )

    best_seller = (
        top_items[0]
        if top_items else None
    )

    category_insights = await get_category_insights(
        db,
        restaurant_id
    )

    rankings = await get_menu_rankings(
        db,
        restaurant_id
    )

    return {

        "best_seller": best_seller,

        "category_insights": category_insights,

        "rankings": rankings
    }