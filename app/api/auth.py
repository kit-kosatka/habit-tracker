from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=201)
async def register(user: UserCreate, session: AsyncSession = Depends(get_db)):
    new_user = await register_user(session, user)
    return new_user

@router.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_db)):
    user = await login_user(session, user)
    return user


