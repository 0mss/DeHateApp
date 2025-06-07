from abc import ABC, abstractmethod
from typing import List

class CommentInterface(ABC):
    @abstractmethod
    async def clean_negative_comments(self, media_ids: List[str]) -> bool:
        ...
