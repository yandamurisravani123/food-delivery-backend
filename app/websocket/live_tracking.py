from fastapi import WebSocket

from app.api.v1.restaurant import router

@router.websocket("/ws/orders/{restaurant_id}")
async def order_stream(websocket: WebSocket, restaurant_id: str):
    await websocket.accept()

    while True:
        await websocket.send_json({
            "event": "new_order",
            "restaurant_id": restaurant_id
        })