from pydantic import BaseModel, RootModel
from typing import Optional, List
from datetime import datetime

class Message(BaseModel):
    content: str
    role: str

class ChatHistory(BaseModel):
    session_id: str
    user_id: str
    title: Optional[str] = None
    created_at: str

class ChatsResponse(BaseModel):
    chats: List[ChatHistory]

class ChatHistoryList(RootModel):
    root: List[ChatHistory]

    def __iter__(self):
        return iter(self.root)

    def __len__(self):
        return len(self.root)