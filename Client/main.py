from colorama import Fore
from utils.pretty import console_welcome, pretty_print
from login import login_or_register
from chat_session import ChatSession
import asyncio
from api_client import APIClient

from services.message_handler import ConsoleMessageHandler
from services.session_manager import WebSocketSessionManager
from services.user_interface import ConsoleUserInterface

async def main():
    console_welcome()
    user_id, username = await login_or_register()
    
    api_client = APIClient()
    async with api_client:
        session_manager = WebSocketSessionManager(api_client, user_id)
        message_handler = ConsoleMessageHandler()
        ui = ConsoleUserInterface()
        
        chat_session = ChatSession(
            session_manager=session_manager,
            message_handler=message_handler,
            ui=ui,
            username=username
        )
        
        await chat_session.start()

if __name__ == "__main__":
    asyncio.run(main())