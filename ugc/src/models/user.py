import uuid
from datetime import datetime

from pydantic import BaseModel


class BookmarkModel(BaseModel):
    movie_id: uuid.UUID


class Comment(BaseModel):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    text: str
    date: datetime
