from typing import List
from fastapi import HTTPException
import google.generativeai as genai
from app.interfaces.llm_interface import LLMInterface
from app.core.config import GEMINI_API_KEY, LLM_MODEL

class GeminiClient(LLMInterface):
    def __init__(self):
        # Configuração da chave da API
        genai.configure(api_key=GEMINI_API_KEY)
        # Configuração do modelo de LLM
        self.model = genai.GenerativeModel(LLM_MODEL)

    async def llm_connection(self, prompt: str) -> List[str]:
        try:
            # Gerando a resposta
            response = self.model.generate_content(prompt)
            # Adicionando IDs de comentários negatívos a uma lista
            list_response = response.text.split()

            return list_response
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Erro ao conectar com llm: {str(e)}"
            )
    