from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.services.habit_service import create_hab, get_hab, update_hab, delete_hab
from app.dependencies.depends import get_current_user
from typing import List


router = APIRouter(prefix="/habits", tags=["habits"])

@router.post("/create", response_model=HabitRead)
async def create(habit_in: HabitCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await create_hab(db=db, habit_in=habit_in, user_id=current_user.id)
    return result

@router.get("/read", response_model=List[HabitRead])
async def get_read_all(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await get_hab(db=db, user_id=current_user.id)
    return result

@router.get("/read/{habit_id}", response_model=HabitRead)
async def get_read(habit_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await get_hab(db=db, user_id=current_user.id, habit_id=habit_id)
    return result

@router.put("/update/{habit_id}", response_model=HabitRead)
async def update(hunit_in: HabitUpdate, habit_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await update_hab(db=db, user_id=current_user.id, habit_id=habit_id, habit_in=hunit_in)
    return result

@router.delete("/delete/{habit_id}")
async def delete(habit_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await delete_hab(db=db, user_id=current_user.id, habit_id=habit_id)
    return {"deleted": "done"}
