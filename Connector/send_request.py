from singleton import AnthropicClient
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from shared.schemas import chat

system_prompt = "You are a dungeon master, you build a story and options for your players to choose from. The players will choose an option and you will continue the story based on their choice. The goal is to create an engaging story for the players to enjoy. If a player faces death or failure then the story ends and you should type __END__ at the end of your response. The player can also win and in that case you type __WIN__, you must always provide the player with options like 1/ 2/ 3/ ... can tell the player that his choice is invalid in case didn't select a valid option."
model = "claude-3-haiku-20240307"

async def get_response(
    messages: chat.Messages
) -> str:
    messages = messages.dict()['messages']
    client = AnthropicClient().get_client()
    message =  client.messages.create(
        max_tokens=1024,
        messages=messages,
        system=system_prompt,
        model=model
    )
    return message.content[0].text