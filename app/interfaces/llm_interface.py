from abc import ABC, abstractmethod
from typing import List

class LLMInterface(ABC):
    @abstractmethod
    async def llm_connection(self, prompt: str) -> List[str]:
        ...
