from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Literal
from app.domain.models.media import MediaType

class MediaBase(BaseModel):
    id: str 
    format: MediaType
    image: str
    title: str
    publish_date: datetime
    view_count: int
    comment_count: int
    like_count: int

class MediaResponse(MediaBase):
    pass

class MediasListResponse(BaseModel):
    videos: List[MediaResponse]
    total: int

class MediaFilterParams(BaseModel):
    format: Optional[MediaType] = None
    min_views: Optional[int] = None
    max_views: Optional[int] = None
    min_comments: Optional[int] = None
    max_comments: Optional[int] = None
    min_likes: Optional[int] = None
    max_likes: Optional[int] = None
    sort_by: Optional[Literal["date","views","comments","likes"]] = "date"
    sort_order: Optional[Literal["asc","desc"]] = "desc"
