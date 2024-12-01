from abc import ABC, abstractmethod
from typing import Protocol, AsyncIterator
from websockets import WebSocketClientProtocol

class IMessageHandler(Protocol):
    async def format(self, message: str) -> str: pass
    async def display(self, message: str) -> None: pass

class ISessionManager(Protocol):
    async def create(self, title: str | None = None) -> str: pass
    async def list(self) -> list[dict]: pass
    async def connect(self, session_id: str) -> WebSocketClientProtocol: pass

class IUserInterface(Protocol):
    def show_menu(self) -> None: pass 
    def show_sessions(self, sessions: list) -> None: pass
    def get_user_input(self, prompt: str) -> str: pass