from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.schemas.habit_log import HabitLogResponse
from app.services.habit_log_service import (
    get_habit_log_service,
    create_habit_log_service,
    delete_habit_log_service,
    calculate_streak,
)
from app.services.habit_service import (
    delete_habit,
    update_habit,
    get_habit,
    create_habit,
)
from app.dependencies.depends import get_current_user
from typing import List

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("/create", response_model=HabitRead)
async def create(
    habit_in: HabitCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await create_habit(db=db, habit_in=habit_in, user_id=current_user.id)
    return result


@router.get("/read", response_model=List[HabitRead])
async def get_read_all(
    limit: int = 10,
    offset: int = 0,
    desc_order: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await get_habit(
        db=db,
        user_id=current_user.id,
        limit=limit,
        offset=offset,
        desc_order=desc_order,
    )
    return result


@router.get("/read/{habit_id}", response_model=HabitRead)
async def get_read(
    habit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await get_habit(db=db, user_id=current_user.id, habit_id=habit_id)
    return result


@router.put("/update/{habit_id}", response_model=HabitRead)
async def update(
    habit_in: HabitUpdate,
    habit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await update_habit(
        db=db, user_id=current_user.id, habit_id=habit_id, habit_in=habit_in
    )
    return result


@router.delete("/delete/{habit_id}")
async def delete(
    habit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await delete_habit(db=db, user_id=current_user.id, habit_id=habit_id)
    return {"deleted": "done"}


@router.get("/{habit_id}/logs", response_model=List[HabitLogResponse])
async def get_habits_logs(
    habit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await get_habit_log_service(db=db, habit_id=habit_id)
    return result


@router.post("/{habit_id}/logs", response_model=HabitLogResponse)
async def create_habits_logs(
    habit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await create_habit_log_service(db=db, habit_id=habit_id)
    return result


@router.delete("/{habit_id}/logs/{log_id}")
async def delete_habit_logs(
    habit_id: int,
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await delete_habit_log_service(db=db, log_id=log_id)
    return {"logs": "deleted"}


@router.get("/{habit_id}/streak")
async def streak(
    habit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    logs = await get_habit_log_service(db=db, habit_id=habit_id)
    check_streak = calculate_streak(logs)
    return {"streak": check_streak}
