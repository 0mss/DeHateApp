from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class MediaType(str, Enum):
    REGULAR = "regular"
    VERTICAL = "vertical"

class Media(BaseModel):
    id: str
    format: MediaType
    image: str
    title: str
    publish_date: datetime
    view_count: int
    comment_count: int
    like_count: int

    class Config:
        orm_mode = True
