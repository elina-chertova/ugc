import uuid
from datetime import datetime

from pydantic import BaseModel


class View(BaseModel):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    view_time: int
    movie_time: int
    event_time: datetime


class Error(BaseModel):
    message: str
    code: int


class Success(BaseModel):
    message: str
    code: int
