from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
    user_presence = await session.execute(select(User).where(User.email == user.email))
    result = user_presence.scalars().first()
    if result:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.post("/login")
async def login_user(user: UserLogin, session: AsyncSession = Depends(get_db)):
    user_presence = await session.execute(select(User).where(User.email == user.email))
    result = user_presence.scalars().first()
    if not result or not verify_password(user.password, result.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {"access_token": token, "refresh_token": refresh_token, "token_type": "bearer"}


