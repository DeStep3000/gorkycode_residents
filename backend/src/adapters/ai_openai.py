from typing import AsyncIterator

from src.protocols.ai_protocol import AIClient


class EchoAIClient(AIClient):
    async def stream_answer(
        self, ticket_id: int, user_message: str, history: list[dict]
    ) -> AsyncIterator[str]:
        text = f"Вы написали: {user_message}"
        # нарезаем по словам
        for word in text.split():
            yield word + " "

    async def complete(
        self, ticket_id: int, user_message: str, history: list[dict]
    ) -> str:
        chunks: list[str] = []
        async for chunk in self.stream_answer(ticket_id, user_message, history):
            chunks.append(chunk)
        return "".join(chunks)
