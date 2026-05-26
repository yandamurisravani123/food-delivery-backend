async def add_to_cart_service(
    request,
    db: AsyncSession
):

    cart_item = Cart(
        user_id=request.user_id,
        food_id=request.food_id,
        quantity=request.quantity
    )

    db.add(cart_item)

    # ADD HERE
    await db.commit()

    await db.refresh(cart_item)

    return cart_item