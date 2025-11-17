from typing import AsyncIterator, Protocol


class AIClient(Protocol):
    async def stream_answer(
        self, ticket_id: int, user_message: str, history: list[dict]
    ) -> AsyncIterator[str]:
        """Вернёт чанки текста ответа."""
        yield ""

    async def complete(
            self, ticket_id: int, user_message: str, history: list[dict]) -> str:
        ...
