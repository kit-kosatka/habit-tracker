from fastapi import HTTPException
from app.crud.habit_logs import (
    create_habit_logs,
    get_habit_logs,
    delete_habit_logs,
    get_habit_log_by_id,
)
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from app.models.habit_log import HabitLog


async def create_habit_log_service(db: AsyncSession, habit_id: int) -> HabitLog:
    existing = await get_habit_logs(db=db, habit_id=habit_id)
    if any(log.date == date.today() for log in existing):
        raise HTTPException(status_code=409, detail="Habit log already exists")
    created_habit = await create_habit_logs(
        db=db, habit_id=habit_id, log_date=date.today(), is_completed=True
    )
    return created_habit


async def get_habit_log_service(db: AsyncSession, habit_id: int) -> list[HabitLog]:
    result = await get_habit_logs(db=db, habit_id=habit_id)
    if not result:
        raise HTTPException(status_code=404, detail="Habit log does not exist")
    return result


async def delete_habit_log_service(db: AsyncSession, log_id: int) -> dict:
    result = await get_habit_log_by_id(db=db, log_id=log_id)
    if not result:
        raise HTTPException(status_code=404, detail="Habit log does not exist")
    await delete_habit_logs(db=db, log_id=log_id)
    return {"habit_log": "deleted"}


def calculate_streak(logs: list[HabitLog]) -> int:
    streak = 0
    check_day = date.today()
    log_dates = {log.date for log in logs}

    while check_day in log_dates:
        streak += 1
        check_day -= timedelta(days=1)

    return streak
