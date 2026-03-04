from fastapi import FastAPI
from app.api.auth import router
from fastapi import FastAPI
from app.api.auth import router
import app.models.user
import app.models.habit
import app.models.habit_log

app = FastAPI()

app.include_router(router)