from typing import List
from app.domain.models.comment import Comment
from app.services.llm.llm_factory import LLMFactory
from app.interfaces.llm_interface import LLMInterface


class LLMService:
    def __init__(self, llm: str):
        # Instancia o client da LLM via factory
        self.llm: LLMInterface = LLMFactory().get_llm(llm)

    async def detect_negative_comments(self, comments: List[Comment]) -> List[str]:
        # Cria uma lista com todos comentário e seus respectivos ids
        context = [f'{comment.id} - {comment.text}' for comment in comments]
        # Transforma a lista em uma string
        context = "\n".join(context)

        # Prompt que será passado para a LLM
        prompt = f'''
        Segue abaixo uma lista de comentários de um vídeo produzido por um criador de conteúdo.
        Antes de cada comentário, tem um "ID".
        Retorne apenas os IDs, separados por um espaço simples, de todos os comentários que:

        - sejam ofensivos,
        - tenham palavras agressivas, sarcásticas ou irônicas,
        - zombem da aparência, do conteúdo ou da pessoa,
        - ou demonstrem rejeição, depreciação ou julgamento negativo, mesmo que em tom leve ou genérico do vídeo.

        Caso nenhum comentário se encaixe nessas premissas, retorne apenas um espaço simples: " "

        (comentários - início)

        {context}

        (comentários - fim)
        '''

        # Retorna lista de ids dos comentários a serem deletados
        return await self.llm.llm_connection(prompt)
