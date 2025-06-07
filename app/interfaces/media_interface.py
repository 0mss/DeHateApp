from abc import ABC, abstractmethod
from typing import List, Tuple
from app.domain.models.media import Media
from app.domain.schemas.media import MediaFilterParams

class MediaInterface(ABC):
    @abstractmethod
    async def filter_medias(self, params: MediaFilterParams) -> Tuple[int, List[Media]]:
        ...
