import random

from sqlalchemy import select

from app.models.food import Food
from app.models.order import Order
from app.models.user_preference import UserPreference
from uuid import UUID

# =====================================================
# GENERATE AI RECOMMENDATIONS
# =====================================================

async def generate_recommendations(
    user_id: UUID,
    db
):

    # -----------------------------------------------------
    # FETCH USER PREFERENCES
    # -----------------------------------------------------

    preference_query = await db.execute(
        select(UserPreference).where(
            UserPreference.user_id == user_id
        )
    )

    preference = preference_query.scalar_one_or_none()

    # -----------------------------------------------------
    # FETCH USER ORDER HISTORY
    # -----------------------------------------------------

    order_query = await db.execute(
        select(Order).where(
            Order.user_id == user_id
        )
    )

    orders = order_query.scalars().all()

    # -----------------------------------------------------
    # GET FAVORITE CUISINES
    # -----------------------------------------------------

    favorite_cuisines = []

    for order in orders:

        if order.cuisine:
            favorite_cuisines.append(
                order.cuisine
            )

    # -----------------------------------------------------
    # FETCH RECOMMENDED FOODS
    # -----------------------------------------------------

    food_query = await db.execute(

        select(Food).where(
            Food.is_recommended == True
        )

    )

    foods = food_query.scalars().all()

    # -----------------------------------------------------
    # GENERATE RECOMMENDATIONS
    # -----------------------------------------------------

    recommendations = []

    for food in foods:

        # MATCH PERCENTAGE

        match_percentage = random.randint(88, 99)

        # BETTER MATCH IF CUISINE MATCHES

        if food.cuisine in favorite_cuisines:

            match_percentage = random.randint(
                95,
                99
            )

        # USER PREFERENCE MATCH

        preference_match = False

        if preference:

            if (
                preference.favorite_cuisine
                and food.cuisine ==
                preference.favorite_cuisine
            ):

                preference_match = True

                match_percentage = 99

        # ADD RECOMMENDATION

        recommendations.append({

            "food_id": food.id,

            "food_name": food.name,

            "description": food.description,

            "image": food.image,

            "category": food.category,

            "cuisine": food.cuisine,

            "rating": food.rating,

            "preparation_time": (
                food.preparation_time
            ),

            "tags": food.tags,

            "match_percentage": (
                match_percentage
            ),

            "ai_reason": (

                f"Perfect match for "
                f"{food.cuisine} lovers"

                if not preference_match

                else

                f"Recommended based on your "
                f"favorite cuisine "
                f"{preference.favorite_cuisine}"
            )
        })

    # -----------------------------------------------------
    # SORT BY MATCH PERCENTAGE
    # -----------------------------------------------------

    recommendations = sorted(

        recommendations,

        key=lambda x: x["match_percentage"],

        reverse=True
    )

    return recommendations