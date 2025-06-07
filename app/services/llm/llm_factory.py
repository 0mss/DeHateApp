from app.infrastructure.clients.gemini_client import GeminiClient
from app.interfaces.llm_interface import LLMInterface

class LLMFactory:
    @staticmethod
    def get_llm(llm: str) -> LLMInterface:
        if llm.lower() == "gemini":
            return GeminiClient()
        else:
            raise ValueError(
                f"LLM '{llm}' não suportada no momento."
            )
        