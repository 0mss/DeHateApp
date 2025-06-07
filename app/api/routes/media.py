from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List

from app.domain.schemas.media import (
    MediaFilterParams,
    MediaResponse,
    MediasListResponse,
)
from app.domain.schemas.responses import DataResponse, ResponseBase
from app.domain.models.media import MediaType
from app.services.media_service import MediaService
from app.services.comment_service import CommentService
from app.api.dependencies import get_media_service, get_comment_service
from app.core.exceptions import InvalidFilterException


router = APIRouter(
    prefix="/medias",
    tags=["Medias"],
)

# Endpoint para listar mídias com filtros e ordenações.
# Exemplo: GET /medias/?format=vertical&sort_by=comments&sort_order=desc&min_views=1000
@router.get("/", response_model=DataResponse[MediasListResponse])
async def get_medias(
    format: MediaType = Query(None, description="Format: regular or vertical"),
    min_views: int = Query(None),
    max_views: int = Query(None),
    min_comments: int = Query(None),
    max_comments: int = Query(None),
    min_likes: int = Query(None),
    max_likes: int = Query(None),
    sort_by: str = Query("date", description="Sort by: date, views, comments, likes"),
    sort_order: str = Query("desc", description="asc or desc"),
    media_service: MediaService = Depends(get_media_service),
):

    params = MediaFilterParams(
        format=format,
        min_views=min_views,
        max_views=max_views,
        min_comments=min_comments,
        max_comments=max_comments,
        min_likes=min_likes,
        max_likes=max_likes,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    try:
        total, medias = await media_service.filter_medias(params)
    except InvalidFilterException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )

    return DataResponse[MediasListResponse](
        success=True,
        message="Mídias listadas com sucesso.",
        data=MediasListResponse(
            videos=[MediaResponse(**media.model_dump()) for media in medias],
            total=total,
        )
    )


@router.post("/clean-comments", response_model=ResponseBase)
async def clean_comments(
    media_ids: List[str],
    comment_service: CommentService = Depends(get_comment_service)
):
    if not media_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A lista de mídias não pode estar vazia."
        )

    try:
        result = await comment_service.clean_negative_comments(media_ids)
        if result:
            return ResponseBase(
                success=True,
                message="Comentários ofensivos removidos com sucesso."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao remover comentários ofensivos."
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
