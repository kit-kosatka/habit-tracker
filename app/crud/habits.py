from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.habit import Habit
from sqlalchemy.orm import joinedload


async def create_habits(db: AsyncSession, title: str, description: str, user_id: int):
    new_habit = Habit(title=title, description=description, user_id=user_id)
    db.add(new_habit)
    await db.commit()
    await db.refresh(new_habit)
    return new_habit

async def get_habits_by_user(db: AsyncSession, user_id: int, limit: int = 10, offset: int = 0, desc_order: bool = True):
    user_habits = select(Habit).where(Habit.user_id == user_id)
    if desc_order:
        user_habits = user_habits.order_by(Habit.id.desc())
    else:
        user_habits = user_habits.order_by(Habit.id.asc())
    user_habits = user_habits.limit(limit).offset(offset)
    result = await db.execute(user_habits)
    return result.scalars().all()

async def get_habit_by_user(db: AsyncSession, user_id: int, habit_id: int):
    user_habit = await db.execute(select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id))
    result = user_habit.scalars().first()
    return result

async def update_habits(db: AsyncSession, user_id: int, habit_id: int, new_title: str, new_description: str):
    habit = await get_habit_by_user(db, user_id, habit_id)
    habit.title = new_title
    habit.description = new_description
    await db.commit()
    await db.refresh(habit)
    return habit


async def delete_habits(db: AsyncSession, user_id: int, habit_id: int):
    habit = await get_habit_by_user(db, user_id, habit_id)
    await db.delete(habit)
    await db.commit()
    return {"habit": "Deleted"}