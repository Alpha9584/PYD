from colorama import Fore
from domain.interfaces import IUserInterface
from utils.pretty import pretty_print

class ConsoleUserInterface(IUserInterface):
    def show_menu(self) -> None:
        pretty_print("\n╔═════ QUEST MENU ═════╗", Fore.GREEN)
        print("1. Start New Quest")
        print("2. Continue Previous Quest")
        print("3. Return to Town (Exit)")
        
    def show_sessions(self, sessions: list) -> None:
        if not sessions:
            pretty_print("No previous quests found!", Fore.YELLOW)
            return
            
        pretty_print("\n╔═════ YOUR QUESTS ═════╗", Fore.GREEN)
        for idx, session in enumerate(sessions, 1):
            title = session.get('title', 'Untitled Quest')
            pretty_print(f"{idx}. {title}", Fore.CYAN)
            
    def get_user_input(self, prompt: str) -> str:
        return input(prompt).strip()