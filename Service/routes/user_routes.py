from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from db.models import User
import sys
from pathlib import Path


project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from shared.schemas.user import User_Login, User_Create
from config import get_async_session
from utils.encryption import encrypt_password, verify_password


async def register_user(
    user_create: User_Create,
    db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    try:        
        if await user_exists(user_create.username, db):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": "User already exists"}
            )
        
        if await email_exists(user_create.email, db):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": "Email already exists"}
            )

        encrypted_password = encrypt_password(user_create.password)
        
        new_user = User(
            username=user_create.username,
            password=encrypted_password,
            email=user_create.email,
            fname=user_create.f_name,
            lname=user_create.l_name
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"user_id": str(new_user.user_id)}
        )

    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Failed to create user: {str(e)}"}
        )

async def user_exists(
    username: str,
    db: AsyncSession = Depends(get_async_session)
) -> bool:
    try:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalars().first() is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def user_exists_by_id(
    user_id: str,
    db: AsyncSession = Depends(get_async_session)
) -> bool:
    try:
        query = select(User).where(User.user_id == user_id)
        result = await db.execute(query)
        return result.scalars().first() is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def email_exists(
    email: str,
    db: AsyncSession = Depends(get_async_session)
) -> bool:
    try:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first() is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def login_user(
    user_login: User_Login,
    db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    try:
        query = select(User).where(User.username == user_login.username)
        result = await db.execute(query)
        user = result.scalars().first()
        
        if not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "User not found"}
            )
            
        if not verify_password(user_login.password, user.password):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid password"}
            )
            
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"user_id": str(user.user_id)}
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Login failed: {str(e)}"}
        )