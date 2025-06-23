from app.services.media_service import MediaService
from app.services.comment_service import CommentService
from app.services.auth_service import AuthService
from app.services.platform.platform_service import PlatformService
from app.services.llm.llm_service import LLMService
from functools import lru_cache

# Função de dependência para injetar o serviço de plataforma
def get_platform_service() -> PlatformService:
    return PlatformService(
        platform="youtube"
    )

# Função de dependência para injetar o serviço de autenticação
# @lru_cache garante que a instância seja reutilizada (singleton)
@lru_cache
def get_auth_service() -> AuthService:
    return AuthService(
        platform="youtube"
    )

# Função de dependência para injetar o serviço de LLM
def get_llm_service() -> LLMService:
    return LLMService(
        llm="gemini"
    )

# Função de dependência para injetar o serviço de mídias
def get_media_service() -> MediaService:
    return MediaService(
        platform_service=get_platform_service()
    )

# Função de dependência para injetar o serviço de comentários
def get_comment_service() -> CommentService:
    return CommentService(
        platform_service=get_platform_service(),
        llm_service=get_llm_service()
    )
