from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Sender, Ticket, Message
from src.adapters.repo_protocols import SenderRepo, TicketRepo, MessageRepo


class SenderRepoImpl(SenderRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Sender | None:
        res = await self.session.execute(select(Sender).where(Sender.email == email))
        return res.scalar_one_or_none()

    async def get_by_id(self, sender_id: int) -> Sender | None:
        res = await self.session.execute(
            select(Sender).where(Sender.id == sender_id)
        )
        return res.scalars().first()

    async def add(self, sender: Sender) -> Sender:
        self.session.add(sender)
        await self.session.flush()
        return sender


class TicketRepoImpl(TicketRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        await self.session.flush()
        return ticket

    async def get_owned(self, ticket_id: int, sender_id: int) -> Ticket | None:
        res = await self.session.execute(
            select(Ticket).where(Ticket.id == ticket_id, Ticket.sender_id == sender_id)
        )
        return res.scalar_one_or_none()

    async def list_by_sender(self, sender_id: int) -> list[Ticket]:
        res = await self.session.execute(
            select(Ticket)
            .where(Ticket.sender_id == sender_id)
            .order_by(Ticket.created_at.desc())
        )
        return list(res.scalars().all())


class MessageRepoImpl(MessageRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, message: Message) -> Message:
        self.session.add(message)
        await self.session.flush()
        return message

    async def list_for_ticket(self, ticket_id: int) -> list[Message]:
        res = await self.session.execute(
            select(Message)
            .where(Message.ticket_id == ticket_id)
            .order_by(Message.created_at)
        )
        return list(res.scalars().all())
