from src.protocols.ai_protocol import AIClient
from src.protocols.repo_protocols import TicketRepo, MessageRepo
from src.db.models import Ticket, Message, MessageRole


class TicketService:
    def __init__(
        self,
        ticket_repo: TicketRepo,
        message_repo: MessageRepo,
        ai_client: AIClient,
    ):
        self.ticket_repo = ticket_repo
        self.message_repo = message_repo
        self.ai_client = ai_client

    async def create_ticket(
        self, sender_id: int, description: str, category_id: int | None, relevance: int
    ) -> Ticket:
        ticket = Ticket(
            description=description,
            sender_id=sender_id,
            category_id=category_id,
            relevance=relevance,
        )
        await self.ticket_repo.add(ticket)

        # первая запись в чате — сообщение пользователя
        msg = Message(
            ticket_id=ticket.id,
            role=MessageRole.user,
            content=description,
        )
        await self.message_repo.add(msg)

        history: list[dict] = []
        ai_text = await self.ai_client.complete(ticket.id, description, history)
        ai_msg = Message(
            ticket_id=ticket.id,
            role=MessageRole.assistant,
            content=ai_text,
        )
        await self.message_repo.add(ai_msg)

        return ticket

    async def list_tickets(self, sender_id: int) -> list[Ticket]:
        return await self.ticket_repo.list_by_sender(sender_id)

    async def list_messages(self, ticket_id: int, sender_id: int):
        ticket = await self.ticket_repo.get_owned(ticket_id, sender_id)
        if not ticket:
            raise PermissionError
        return await self.message_repo.list_for_ticket(ticket_id)
