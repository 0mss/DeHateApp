from app.services.platform.platform_factory import PlatformFactory
from app.interfaces.auth_interface import AuthInterface

class AuthService(AuthInterface):
    def __init__(self, platform: str):
        self.platform: AuthInterface = PlatformFactory().get_platform(platform)

    async def get_login_url(self) -> str:
        return await self.platform.get_login_url()

    async def handle_callback(self, code: str) -> bool:
        return await self.platform.handle_callback(code)
    