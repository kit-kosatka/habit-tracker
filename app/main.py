from fastapi import FastAPI
from app.api.auth import router
from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.habits import router as habits_router
import app.models.user
import app.models.habit
import app.models.habit_log

app = FastAPI()

app.include_router(auth_router)

app.include_router(habits_router)