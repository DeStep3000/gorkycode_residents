from datetime import datetime

from pydantic import BaseModel, Field

from src.db.models import Ticket, Message


class TicketCreateRequest(BaseModel):
    description: str = Field(..., max_length=65000)
    category_id: int | None = None
    relevance: int = Field(5, ge=1, le=10)


class TicketResponse(BaseModel):
    id: int
    description: str
    created_at: datetime
    relevance: int

    @staticmethod
    def from_db(ticket: Ticket) -> "TicketResponse":
        return TicketResponse(
            id=ticket.id,
            description=ticket.description,
            created_at=ticket.created_at,
            relevance=ticket.relevance,
        )


class ManyTicketsResponse(BaseModel):
    tickets: list[TicketResponse]

    @staticmethod
    def from_db(tickets: list[Ticket]) -> "ManyTicketsResponse":
        return ManyTicketsResponse(
            tickets=[
                TicketResponse(
                    id=ticket.id,
                    description=ticket.description,
                    created_at=ticket.created_at,
                    relevance=ticket.relevance,
                )
                for ticket in tickets
            ]
        )


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    @staticmethod
    def from_db(msg: Message) -> "MessageResponse":
        return MessageResponse(
            id=msg.id,
            role=msg.role,
            created_at=msg.created_at,
            content=msg.content,
        )


class ManyMessagesResponse(BaseModel):
    messages: list[MessageResponse]

    @staticmethod
    def from_db(msgs: list[Message]) -> "ManyMessagesResponse":
        return ManyMessagesResponse(
            messages=[
                MessageResponse(
                    id=msg.id,
                    role=msg.role,
                    created_at=msg.created_at,
                    content=msg.content,
                )
                for msg in msgs
            ]
        )
