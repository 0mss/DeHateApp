from typing import List
from app.services.platform.platform_factory import PlatformFactory
from app.interfaces.platform_interface import PlatformInterface
from app.domain.models.media import Media
from app.domain.models.comment import Comment


class PlatformService(PlatformInterface):
    def __init__(self, platform: str):
        self.platform: PlatformInterface = PlatformFactory().get_platform(platform)

    async def fetch_medias(self) -> List[Media]:
        return await self.platform.fetch_medias()

    async def fetch_comments(self, media_id: str) -> List[Comment]:
        return await self.platform.fetch_comments(media_id)

    async def delete_comments(self, comment_ids: List[str]) -> bool:
        return await self.platform.delete_comments(comment_ids)
