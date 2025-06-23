from typing import List
from app.interfaces.llm_interface import LLMInterface
from app.interfaces.comment_interface import CommentInterface
from app.interfaces.platform_interface import PlatformInterface


class CommentService(CommentInterface):
    def __init__(self,
        platform_service: PlatformInterface,
        llm_service: LLMInterface,
    ):
        self.platform_service = platform_service
        self.llm_service = llm_service


    # Recebe uma lista de IDs de mídias selecionadas
    # faz todo o processo de limpeza dos comentários negatívos.
    async def clean_negative_comments(self, media_ids: List[str]) -> bool:
        try:
            for media_id in media_ids:
                comments = await self.platform_service.fetch_comments(media_id)

                negative_comments_ids = None

                if comments:
                    negative_comments_ids = await self.llm_service.detect_negative_comments(comments)

                if negative_comments_ids:
                    success = await self.platform_service.delete_comments(negative_comments_ids)

                    if not success:
                        raise Exception(f"Falha ao deletar comentários da mídia {media_id}")

            return True

        except Exception as e:
            raise Exception(f"Erro na limpeza de comentários: {str(e)}")
