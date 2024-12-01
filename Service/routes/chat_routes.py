from fastapi import Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
from sqlmodel import select
from db.models import ChatHistory, SessionStatus
from shared.schemas.chat import Message, Messages, Chat, Chats, Chat_History, SessionResponse, CreateSession, SendMessage
from typing import List
from config import get_async_session
from utils.connection import manager
from .user_routes import user_exists_by_id
import sys
from pathlib import Path
from datetime import datetime
import aiohttp
import json
import os

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

async def user_sessions(
    user_id: str,
    db: AsyncSession = Depends(get_async_session)
) -> List[Chat_History]:
    try:
        found_user = await user_exists_by_id(user_id, db)
        if not found_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        query = select(ChatHistory).where(ChatHistory.user_id == user_id).order_by(ChatHistory.created_at)
        
        await db.connection()
        result = await db.execute(
            query,
            execution_options={"compiled_cache": None}
        )
        
        chat_histories = result.scalars().all() 
        response = [Chat_History.from_orm(chat) for chat in chat_histories]
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve sessions: {str(e)}"
        )

async def create_session(
    createSession: CreateSession,
    db: AsyncSession = Depends(get_async_session)
) -> SessionResponse:
    try:
        found_user = await user_exists_by_id(createSession.user_id, db)
        if not found_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )


        new_chat = ChatHistory(
            user_id=createSession.user_id,
            title=createSession.title or "New Chat",
            created_at=datetime.now(),
            status=SessionStatus.IN_PROGRESS.value
        )

        db.add(new_chat) 
        await db.commit()
        return SessionResponse(session_id=str(new_chat.session_id))
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create session"
        )
    
async def session_exists(
    session_id: str,
    db: AsyncSession = Depends(get_async_session)
) -> bool:
    try:
        query = select(ChatHistory).where(ChatHistory.session_id == session_id)
        result = await db.execute(query)
        return result.scalars().first() is not None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check session"
        )

async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_async_session)
) -> Chat:
    try:
        found_session = await session_exists(session_id, db)
        if not found_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        query = select(ChatHistory).where(ChatHistory.session_id == session_id)
        result = await db.execute(query)
        chat = result.scalars().first()
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        return Chat.from_orm(chat)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve session"
        )
    
async def add_message(
    session_id: str,
    message: Message,
    db: AsyncSession = Depends(get_async_session)
) -> Response:
    try:
        query = select(ChatHistory).where(ChatHistory.session_id == session_id)
        result = await db.execute(query)
        chat = result.scalars().first()
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        if chat.messages is None:
            chat.messages = {"messages": []}
        
        if isinstance(chat.messages, str):
            chat.messages = json.loads(chat.messages)
        if not isinstance(chat.messages, dict):
            chat.messages = {"messages": []}
            
        message_dict = message.dict()
        chat.messages["messages"].append(message_dict)
        
        db.add(chat)
        flag_modified(chat, "messages")
        
        await db.commit()
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add message: {str(e)}"
        )
    
async def send_message(
    sendMessage: SendMessage,
    db: AsyncSession = Depends(get_async_session)
) -> Message:
    try:
        found_session = await session_exists(sendMessage.session_id, db)
        if not found_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        user_message = Message(role="user", content=sendMessage.message)
        await add_message(sendMessage.session_id, user_message, db)

        chat = await get_session(sendMessage.session_id, db)
        
        messages_json = {
            "messages": [msg.dict() for msg in chat.messages]
        }
        
        connector_url = os.getenv("Connector_URL")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{connector_url}/chat/send",
                json=messages_json
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to get response from connector"
                    )
                ai_response = await response.text()

        assistant_message = Message(role="assistant", content=ai_response)
        await add_message(sendMessage.session_id, assistant_message, db)

        return assistant_message

    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Connector service unavailable"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )
    
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
    session_id: str,
    db: AsyncSession = Depends(get_async_session)
):
    client_id = f"{user_id}_{session_id}"
    
    try:
        found_session = await session_exists(session_id, db)
        if not found_session:
            await websocket.close(code=4004)
            return

        await manager.connect(websocket, client_id)
        
        try:
            while True:
                data = await websocket.receive_text()
                
                if data.upper() == "EXIT":
                    await websocket.send_text("Chat session ended")
                    break
                
                send_msg = SendMessage(
                    user_id=user_id,
                    session_id=session_id,
                    message=data
                )
                
                response = await send_message(send_msg, db)
                await websocket.send_text(response.content)
                
        except WebSocketDisconnect:
            manager.disconnect(client_id)
            
    except Exception as e:
        error_msg = str(e)[:100]
        await websocket.close(code=4000, reason=error_msg)