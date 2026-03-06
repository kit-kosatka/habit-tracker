from sqlalchemy import select
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user