from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections = {}


    async def connect(
        self,
        user_id: str,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections[user_id] = websocket


    def disconnect(self, user_id: str):

        self.active_connections.pop(user_id, None)


    async def send_notification(
        self,
        user_id: str,
        message: dict
    ):

        websocket = self.active_connections.get(user_id)

        if websocket:
            await websocket.send_json(message)


manager = ConnectionManager()