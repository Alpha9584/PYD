from typing import AsyncIterator
from domain.interfaces import IMessageHandler, ISessionManager, IUserInterface
from services.message_handler import ConsoleMessageHandler
from services.session_manager import WebSocketSessionManager
from utils.pretty import pretty_print
from colorama import Fore

class ChatSession:
    def __init__(
        self,
        session_manager: ISessionManager,
        message_handler: IMessageHandler,
        ui: IUserInterface,
        username: str
    ):
        self.session_manager = session_manager
        self.message_handler = message_handler
        self.ui = ui
        self.username = username

    async def start(self):
        while True:
            self.ui.show_menu()
            choice = self.ui.get_user_input("=> ")
            
            actions = {
                "1": self.create_new_session,
                "2": self.list_sessions,
                "3": self.exit_session
            }
            
            if action := actions.get(choice):
                await action()

    async def create_new_session(self):
        title = self.ui.get_user_input("Name your quest (or press Enter for default): ")
        session_id = await self.session_manager.create(title)
        await self.start_chat(session_id)

    async def start_chat(self, session_id: str):
        ws = await self.session_manager.connect(session_id)
        pretty_print("\nChat session started! (Type 'EXIT' to end)", Fore.GREEN)
        
        try:
            async for message in self._chat_loop(ws):
                formatted = await self.message_handler.format(message)
                await self.message_handler.display(formatted)
        finally:
            await ws.close()

    async def _chat_loop(self, ws) -> AsyncIterator[str]:
        while True:
            message = self.ui.get_user_input(f"{self.username}> ")
            if message.upper() == "EXIT":
                break
                
            await ws.send(message)
            yield await ws.recv()

    async def list_sessions(self):
        sessions = await self.session_manager.list()
        self.ui.show_sessions(sessions)
        
        if not sessions:
            return
            
        choice = self.ui.get_user_input("Select a quest number (or press Enter to go back): ")
        if choice.isdigit() and 0 < int(choice) <= len(sessions):
            session_id = sessions[int(choice)-1]["session_id"]
            await self.start_chat(session_id)

    async def exit_session(self):
        pretty_print("\nFarewell brave adventurer!", Fore.YELLOW)
        raise SystemExit(0)