from domain.interfaces import ISessionManager
from websockets import WebSocketClientProtocol
from api_client import APIClient

class WebSocketSessionManager(ISessionManager):
    def __init__(self, client: APIClient, user_id: str):
        self.client = client
        self.user_id = user_id

    async def create(self, title: str | None = None) -> str:
        response = await self.client.create_session(self.user_id, title)
        return response["session_id"]

    async def list(self) -> list[dict]:
        return await self.client.get_user_sessions(self.user_id)

    async def connect(self, session_id: str) -> WebSocketClientProtocol:
        return await self.client.connect_websocket(self.user_id, session_id)