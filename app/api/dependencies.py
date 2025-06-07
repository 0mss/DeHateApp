from app.services.media_service import MediaService
from app.services.comment_service import CommentService
from app.services.auth_service import AuthService
from app.services.platform.platform_service import PlatformService
from app.services.llm.llm_service import LLMService

def get_platform_service() -> PlatformService:
    return PlatformService(
        platform="youtube"
    )

def get_auth_service() -> AuthService:
    return AuthService(
        platform="youtube"
    )

def get_llm_service() -> LLMService:
    return LLMService(
        llm="gemini"
    )

def get_media_service() -> MediaService:
    return MediaService(
        platform_service=get_platform_service()
    )

def get_comment_service() -> CommentService:
    return CommentService(
        platform_service=get_platform_service(),
        llm_service=get_llm_service()
    )
