from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum
import json

class Role(str, Enum):
    user = "user"
    assistant = "assistant"

class Message(BaseModel):
    content: str
    role: Role

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        return {
            "content": self.content,
            "role": self.role
        }
    
    def json(self) -> str:
        return json.dumps(self.dict())

class Messages(BaseModel):
    messages: list[Message]

class Chat(BaseModel):
    session_id: str
    user_id: str
    title: Optional[str]
    messages: list[Message] = Field(default_factory=list)
    created_at: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, orm_obj):
        try:
            if isinstance(orm_obj.messages, dict):
                messages_data = orm_obj.messages.get("messages", [])
            elif isinstance(orm_obj.messages, str):
                messages_data = json.loads(orm_obj.messages).get("messages", [])
            else:
                messages_data = orm_obj.messages

            # Convert each message to Message object
            messages = []
            for msg in messages_data:
                if isinstance(msg, dict):
                    messages.append(Message(
                        content=msg.get("content", ""),
                        role=msg.get("role", "user")
                    ))
                elif isinstance(msg, Message):
                    messages.append(msg)

            return cls(
                session_id=str(orm_obj.session_id),
                user_id=str(orm_obj.user_id),
                title=orm_obj.title,
                created_at=orm_obj.created_at.isoformat(),
                messages=messages
            )
        except Exception as e:
            raise ValueError(f"Failed to parse messages: {str(e)}")
        

class Chats(BaseModel):
    chats: list[Chat]

class Chat_History(BaseModel):
    session_id: str
    user_id: str
    title: Optional[str]
    created_at: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            session_id=str(orm_obj.session_id),
            user_id=str(orm_obj.user_id),
            title=orm_obj.title,
            created_at=orm_obj.created_at.isoformat()
        )
    
class CreateSession(BaseModel):
    user_id: str
    title: Optional[str]

class SessionResponse(BaseModel):
    session_id: str

class SendMessage(BaseModel):
    session_id: str
    user_id: str
    message: str