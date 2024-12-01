from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, UUID, DateTime, text, ForeignKey, JSON, Enum as SQLAlchemyEnum
from datetime import datetime
import enum
from typing import Optional
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from shared.schemas.chat import Messages

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    fname = Column(String)
    lname = Column(String)
    survived_count = Column(Integer, default=0)
    dead_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now())

class SessionStatus(enum.Enum):
    SURVIVED = "SURVIVED"
    DEAD = "DEAD" 
    IN_PROGRESS = "IN_PROGRESS"

class ChatHistory(Base):
    __tablename__ = 'chat_histories'
    session_id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID, ForeignKey('users.user_id'), nullable=False)
    title = Column(String, nullable=False)
    messages = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    status = Column(SQLAlchemyEnum(SessionStatus, name='session_status'), 
                   nullable=False, 
                   server_default=SessionStatus.IN_PROGRESS.value)