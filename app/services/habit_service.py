from fastapi import HTTPException
from app.crud.habits import create_habits, update_habits, delete_habits, get_habit_by_user, get_habits_by_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.habit import HabitCreate, HabitUpdate


async def create_hab(db: AsyncSession, habit_in: HabitCreate, user_id):
    new_habit = await create_habits(db=db,title=habit_in.title, description=habit_in.description, user_id=user_id)
    return new_habit

async def get_hab(db: AsyncSession, user_id: int, habit_id: int | None = None):
    if habit_id is None:
        get_habits = await get_habits_by_user(db=db, user_id=user_id)
        return get_habits
    else:
        get_habits = await get_habit_by_user(db=db, user_id=user_id, habit_id=habit_id)
        if get_habits is None:
            raise HTTPException(status_code=404)
        return get_habits

async def update_hab(db: AsyncSession, user_id: int, habit_id: int, habit_in: HabitUpdate):
    habit = await get_habit_by_user(db=db, user_id=user_id, habit_id=habit_id)
    if habit is None:
        raise HTTPException(status_code=404)
    update_habit = await update_habits(db=db, user_id=user_id, habit_id=habit_id, new_title=habit_in.title, new_description=habit_in.description)
    return update_habit

async def delete_hab(db: AsyncSession, user_id: int, habit_id: int):
    habit = await get_habit_by_user(db=db, user_id=user_id, habit_id=habit_id)
    if habit is None:
        raise HTTPException(status_code=404)
    deleted_hab = await delete_habits(db=db,user_id=user_id, habit_id=habit_id)
    return {"deleted": "completed"}