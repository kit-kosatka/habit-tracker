from fastapi import HTTPException
from app.crud.habits import (
    create_habits,
    update_habits,
    delete_habits,
    get_habit_by_user,
    get_habits_by_user,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate


async def create_habit(db: AsyncSession, habit_in: HabitCreate, user_id: int) -> Habit:
    return await create_habits(
        db=db, title=habit_in.title, description=habit_in.description, user_id=user_id
    )


async def get_habit(
    db: AsyncSession,
    user_id: int,
    habit_id: int | None = None,
    limit: int = 10,
    offset: int = 0,
    desc_order: bool = True,
) -> list[Habit]:
    if habit_id is None:
        return await get_habits_by_user(
            db=db, user_id=user_id, limit=limit, offset=offset, desc_order=desc_order
        )
    habit = await get_habit_by_user(db=db, user_id=user_id, habit_id=habit_id)
    if habit is None:
        raise HTTPException(status_code=404)
    return habit


async def update_habit(
    db: AsyncSession, user_id: int, habit_id: int, habit_in: HabitUpdate
) -> Habit:
    habit = await get_habit_by_user(db=db, user_id=user_id, habit_id=habit_id)
    if habit is None:
        raise HTTPException(status_code=404)
    return await update_habits(
        db=db,
        user_id=user_id,
        habit_id=habit_id,
        new_title=habit_in.title,
        new_description=habit_in.description,
    )


async def delete_habit(db: AsyncSession, user_id: int, habit_id: int) -> dict:
    habit = await get_habit_by_user(db=db, user_id=user_id, habit_id=habit_id)
    if habit is None:
        raise HTTPException(status_code=404)
    await delete_habits(db=db, user_id=user_id, habit_id=habit_id)
    return {"deleted": "completed"}
