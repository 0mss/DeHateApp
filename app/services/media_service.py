from typing import List, Tuple
from app.domain.models.media import Media
from app.domain.schemas.media import MediaFilterParams
from app.interfaces.media_interface import MediaInterface
from app.interfaces.platform_interface import PlatformInterface
from app.core.exceptions import InvalidFilterException


class MediaService(MediaInterface):
    def __init__(self, platform_service: PlatformInterface):
        self.platform_service = platform_service


    # Valida os filtros, define se as mídias se encaixam
    # nos parametros min e max definidos pelo client e as ordena.
    async def filter_medias(self, params: MediaFilterParams) -> Tuple[int, List[Media]]:
        self._validate_filters(params)

        all_medias = await self.platform_service.fetch_medias()

        filtered_medias = [
            media for media in all_medias
            if self._media_matches_filters(media, params)
        ]

        total = len(filtered_medias)

        sorted_medias = self._sort_medias(filtered_medias, params)

        return total, sorted_medias


    # Métodos auxiliares internos:
    # Validação de filtros: Verifica se algum parâmetro mínimo é maior que o máximo.
    def _validate_filters(self, params: MediaFilterParams) -> None:
        if (
            params.min_views is not None
            and params.max_views is not None
            and params.min_views > params.max_views
        ):
            raise InvalidFilterException(
                "O número mínimo de visualizações não pode ser maior que o máximo."
            )

        if (
            params.min_comments is not None
            and params.max_comments is not None
            and params.min_comments > params.max_comments
        ):
            raise InvalidFilterException(
                "O número mínimo de comentários não pode ser maior que o máximo."
            )

        if (
            params.min_likes is not None
            and params.max_likes is not None
            and params.min_likes > params.max_likes
        ):
            raise InvalidFilterException(
                "O número mínimo de curtidas não pode ser maior que o máximo."
            )


    # Verifica quais mídias se encaixam nos filtros
    # mínimos e máximos dos parâmetros definidos pelo client.
    def _media_matches_filters(self, media: Media, params: MediaFilterParams) -> bool:
        if params.format and media.format != params.format:
            return False

        if params.min_views is not None and media.view_count < params.min_views:
            return False
        if params.max_views is not None and media.view_count > params.max_views:
            return False

        if params.min_comments is not None and media.comment_count < params.min_comments:
            return False
        if params.max_comments is not None and media.comment_count > params.max_comments:
            return False

        if params.min_likes is not None and media.like_count < params.min_likes:
            return False
        if params.max_likes is not None and media.like_count > params.max_likes:
            return False

        return True


    # Ordena a lista de mídias pelo que foi escolhido no frontend:
    # data(crescente ou decrescente), visualizações, comentários ou curtidas. 
    def _sort_medias(self, medias: List[Media], params: MediaFilterParams) -> List[Media]:
        reverse = params.sort_order == "desc"

        if params.sort_by == "date":
            return sorted(medias, key=lambda x: x.publish_date, reverse=reverse)
        elif params.sort_by == "views":
            return sorted(medias, key=lambda x: x.view_count, reverse=reverse)
        elif params.sort_by == "comments":
            return sorted(medias, key=lambda x: x.comment_count, reverse=reverse)
        elif params.sort_by == "likes":
            return sorted(medias, key=lambda x: x.like_count, reverse=reverse)
        else:
            return medias
        