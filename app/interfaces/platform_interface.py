from abc import ABC, abstractmethod
from typing import List
from app.domain.models.media import Media
from app.domain.models.comment import Comment

class PlatformInterface(ABC):
    @abstractmethod
    async def fetch_medias(self) -> List[Media]:
        ...

    @abstractmethod
    async def fetch_comments(self, id_media: str) -> List[Comment]:
        ...

    @abstractmethod
    async def delete_comments(self, comment_ids: List[str]) -> bool:
        ...
