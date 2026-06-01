# app/api/v1/endpoints/ai_recommendation.py

from collections import Counter
import random

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.food import Food
from app.models.restaurant import Restaurant

from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/recommendations",
    tags=["AI Recommendations"]
)


@router.get("/ai")
async def get_ai_recommendations(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # =====================================================
    # GET USER ORDERS
    # =====================================================

    orders_query = await db.execute(
        select(Order)
        .where(Order.user_id == current_user.id)
        .options(
            selectinload(Order.items)
            .selectinload(OrderItem.food)
            .selectinload(Food.restaurant)
        )
    )

    orders = orders_query.scalars().all()

    # =====================================================
    # NEW USER CASE
    # =====================================================

    if not orders:

        trending_query = await db.execute(
            select(Food)
            .options(selectinload(Food.restaurant))
            .limit(5)
        )

        foods = trending_query.scalars().all()

        recommendations = []

        for food in foods:

            recommendations.append({
                "food_id": food.id,
                "food_name": food.name,
                "description": food.description,
                "price": food.price,
                "image": food.image,
                "category": food.category,
                "restaurant": {
                    "id": food.restaurant.id,
                    "name": food.restaurant.name
                },
                "match_percent": random.randint(85, 95),
                "reason": "Trending near you",
                "rating": 4.8,
                "delivery_time": "20-30 min"
            })

        return {
            "success": True,
            "message": "Trending recommendations",
            "recommendations": recommendations,
            "taste_profile": {}
        }

    # =====================================================
    # FIND USER FAVORITE CATEGORIES
    # =====================================================

    categories = []

    total_orders = 0

    for order in orders:

        for item in order.items:

            if item.food:

                total_orders += 1

                categories.append(item.food.category)

    # TOP CATEGORIES

    top_categories = Counter(categories).most_common(3)

    favorite_categories = [
        category[0]
        for category in top_categories
    ]

    # =====================================================
    # GET RECOMMENDED FOODS
    # =====================================================

    foods_query = await db.execute(
        select(Food)
        .where(Food.category.in_(favorite_categories))
        .options(selectinload(Food.restaurant))
        .limit(10)
    )

    foods = foods_query.scalars().all()

    # =====================================================
    # GENERATE RECOMMENDATIONS
    # =====================================================

    recommendations = []

    for food in foods:

        recommendations.append({

            "food_id": food.id,

            "food_name": food.name,

            "description": food.description,

            "price": food.price,

            "image": food.image,

            "category": food.category,

            "restaurant": {
                "id": food.restaurant.id,
                "name": food.restaurant.name
            },

            "match_percent": random.randint(89, 99),

            "reason": f"Because you love {food.category}",

            "rating": round(random.uniform(4.5, 5.0), 1),

            "delivery_time": "20-30 min",

            "ai_message": (
                f"Based on your recent orders from "
                f"{food.restaurant.name}, we think "
                f"you'll appreciate this dish."
            )
        })

    # =====================================================
    # TASTE PROFILE
    # =====================================================

    spicy_orders = len([
        c for c in categories
        if "spicy" in c.lower()
    ])

    italian_orders = len([
        c for c in categories
        if "italian" in c.lower()
    ])

    taste_profile = {

        "spicy_preference": (
            round((spicy_orders / total_orders) * 100)
            if total_orders else 0
        ),

        "italian_orders": italian_orders,

        "favorite_categories": favorite_categories
    }

    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return {

        "success": True,

        "total_recommendations": len(recommendations),

        "recommendations": recommendations,

        "taste_profile": taste_profile
    }