from domain.interfaces import IMessageHandler
import sys
import asyncio
from colorama import Fore

class ConsoleMessageHandler(IMessageHandler):
    async def format(self, message: str) -> str:
        message = message.strip('"').replace('\\n', '\n')
        return self._format_paragraphs(message.split('\n\n'))
        
    async def display(self, message: str) -> None:
        for char in message:
            sys.stdout.write(char)
            sys.stdout.flush()
            await asyncio.sleep(0.03)
        sys.stdout.write('\n')
        
    def _format_paragraphs(self, paragraphs: list[str]) -> str:
        formatted = []
        for para in paragraphs:
            if '"' in para:
                formatted.extend(self._format_dialog(para))
            else:
                formatted.append(f"{Fore.WHITE}{para}")
        return '\n\n'.join(formatted)

    def _format_dialog(self, para: str) -> list[str]:
        parts = para.split('"')
        return [
            f"{Fore.CYAN}\"{part}\"{Fore.WHITE}" if i % 2 else part 
            for i, part in enumerate(parts)
        ]