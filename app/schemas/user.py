from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints
from typing import Annotated


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
