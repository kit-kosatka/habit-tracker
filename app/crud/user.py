from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User


async def get_user_by_email(session: AsyncSession, email: str):
    get_email = await session.execute(select(User).where(User.email == email))
    result = get_email.scalars().first()
    return result

async def create_user(session: AsyncSession, email: str, hashed_password: str):
    new_user = User(email=email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
