
import aiohttp
import asyncio
import websockets
from config import API_BASE_URL, WS_BASE_URL

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.ws_base_url = WS_BASE_URL
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
            
    async def login(self, username: str, password: str):
        async with self.session.post(
            f"{self.base_url}/users/login",
            json={"username": username, "password": password}
        ) as response:
            return await response.json()
            
    async def register(self, user_data: dict):
        async with self.session.post(
            f"{self.base_url}/users/register",
            json=user_data
        ) as response:
            return await response.json()
            
    async def create_session(self, user_id: str, title: str = None):
        async with self.session.post(
            f"{self.base_url}/chat/sessions",
            json={"user_id": user_id, "title": title}
        ) as response:
            return await response.json()
            
    async def get_user_sessions(self, user_id: str):
        async with self.session.get(
            f"{self.base_url}/chat/sessions/{user_id}"
        ) as response:
            return await response.json()
            
    async def connect_websocket(self, user_id: str, session_id: str):
        uri = f"{self.ws_base_url}/ws/{user_id}/{session_id}"
        return await websockets.connect(uri)