from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.habit_log import HabitLog
from datetime import date
from sqlalchemy import Sequence


async def create_habit_logs(
    db: AsyncSession, habit_id: int, log_date: date, is_completed: bool
) -> HabitLog:
    habit_log = HabitLog(habit_id=habit_id, date=log_date, is_completed=is_completed)
    db.add(habit_log)
    await db.commit()
    await db.refresh(habit_log)
    return habit_log


async def get_habit_logs(db: AsyncSession, habit_id: int) -> Sequence[HabitLog]:
    habit_log = await db.execute(select(HabitLog).where(HabitLog.habit_id == habit_id))
    result = habit_log.scalars().all()
    return result


async def delete_habit_logs(db: AsyncSession, log_id: int) -> None:
    habit_log = await db.execute(select(HabitLog).where(HabitLog.id == log_id))
    result = habit_log.scalars().first()
    await db.delete(result)
    await db.commit()


async def get_habit_log_by_id(db: AsyncSession, log_id: int) -> HabitLog | None:
    result = await db.execute(select(HabitLog).where(HabitLog.id == log_id))
    return result.scalars().first()
