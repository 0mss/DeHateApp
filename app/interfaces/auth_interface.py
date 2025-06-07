from abc import ABC, abstractmethod

class AuthInterface(ABC):
    @abstractmethod
    async def get_login_url(self) -> str:
        ...

    @abstractmethod
    async def handle_callback(self, code: str) -> bool:
        ...
