from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import inject, FromDishka

from src.api.deps import get_current_user
from src.db.models import Sender
from src.dto.tickets import (
    TicketCreateRequest,
    TicketResponse,
    ManyTicketsResponse,
    ManyMessagesResponse,
)
from src.services.tickets import TicketService

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


@router.post("")
@inject
async def create_ticket(
    data: TicketCreateRequest,
    service: FromDishka[TicketService],
    current_user: Sender = Depends(get_current_user),
) -> TicketResponse:
    ticket = await service.create_ticket(
        sender_id=current_user.id,
        description=data.description,
        category_id=data.category_id,
        relevance=data.relevance,
    )
    return TicketResponse.from_db(ticket)


@router.get("")
@inject
async def list_tickets(
    service: FromDishka[TicketService],
    current_user: Sender = Depends(get_current_user),
) -> ManyTicketsResponse:
    tickets = await service.list_tickets(current_user.id)
    return ManyTicketsResponse.from_db(tickets)


@router.get("/{ticket_id}/messages")
@inject
async def list_messages(
    ticket_id: int,
    service: FromDishka[TicketService],
    current_user: Sender = Depends(get_current_user),
) -> ManyMessagesResponse:
    try:
        msgs = await service.list_messages(ticket_id, current_user.id)
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return ManyMessagesResponse.from_db(msgs)
