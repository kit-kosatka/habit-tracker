from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token


async def register_user(session: AsyncSession, user_data: UserCreate):
    user = await get_user_by_email(session, user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user_data.password)
    new_user = await create_user(session, user_data.email, hashed_password)
    return new_user

async def login_user(session: AsyncSession, user_data: UserLogin):
    user = await get_user_by_email(session, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {"token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
