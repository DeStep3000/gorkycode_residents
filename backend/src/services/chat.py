from typing import AsyncIterator

from src.adapters.ai_protocol import AIClient
from src.adapters.repo_protocols import TicketRepo, MessageRepo
from src.db.models import Message, MessageRole


class ChatService:
    def __init__(
        self,
        ai_client: AIClient,
        ticket_repo: TicketRepo,
        message_repo: MessageRepo,
    ):
        self.ai_client = ai_client
        self.ticket_repo = ticket_repo
        self.message_repo = message_repo

    async def stream_ai_answer(
        self,
        ticket_id: int,
        sender_id: int,
        user_message: str,
    ) -> AsyncIterator[str]:
        ticket = await self.ticket_repo.get_owned(ticket_id, sender_id)
        if not ticket:
            raise PermissionError

        # сохраняем сообщение пользователя
        user_msg = Message(
            ticket_id=ticket.id,
            role=MessageRole.user,
            content=user_message,
        )
        await self.message_repo.add(user_msg)

        history = []  # можно подтягивать из MessageRepo

        chunks = []
        async for chunk in self.ai_client.stream_answer(
            ticket_id, user_message, history
        ):
            chunks.append(chunk)
            yield chunk

        full_answer = "".join(chunks)
        ai_msg = Message(
            ticket_id=ticket.id,
            role=MessageRole.assistant,
            content=full_answer,
        )
        await self.message_repo.add(ai_msg)
