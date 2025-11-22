from typing import Annotated, List
from datetime import datetime

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from dishka.integrations.fastapi import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_session
from src.schemas.complaint import ComplaintStatus
from src.services.complaints import ComplaintService

router = APIRouter(
    prefix="/api",
    tags=["tickets_front"],  # чисто для группировки в docs
)

SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ======== Pydantic-схемы для фронта ========

class TicketCreate(BaseModel):
    description: str
    category_id: int | None = None
    relevance: int = 5  # фронт всегда шлёт 5, пока просто прокидываем


class TicketRead(BaseModel):
    id: int
    description: str
    created_at: datetime
    relevance: int


class MessageCreate(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class MessageRead(BaseModel):
    id: int | None = None
    role: str
    content: str
    created_at: datetime | None = None


# ======== 1) создание тикета (форма /new) ========

@router.post("/tickets/", response_model=TicketRead)
@inject
async def create_ticket(
    payload: TicketCreate,
    db: SessionDep,
    complaint_service: FromDishka[ComplaintService],
):
    """
    Адаптер: принимает JSON от фронта и создаёт Complaint в БД.
    """
    complaint = await complaint_service.create_complaint(
        db,
        description=payload.description,
        district=str(payload.category_id or ""),      # временно кладём category_id как строку
        status=ComplaintStatus.NEW,
        executor_id=None,
        address="",                                   # можно потом нормально заполнить
    )

    # Вернём структуру в формате, который ждёт фронт
    return TicketRead(
        id=complaint.complaint_id,
        description=complaint.description,
        created_at=complaint.created_at,
        relevance=payload.relevance,
    )


# ======== 2) список тикетов (страница /tickets) ========

@router.get("/tickets", response_model=List[TicketRead])
@inject
async def list_tickets(
    db: SessionDep,
    complaint_service: FromDishka[ComplaintService],
):
    """
    Отдаём последние жалобы как список тикетов.
    """
    complaints = await complaint_service.list_complaints(db, limit=100, offset=0)

    # Если надо, можно сортировать по created_at убыванию
    complaints_sorted = sorted(complaints, key=lambda c: c.created_at, reverse=True)

    return [
        TicketRead(
            id=c.complaint_id,
            description=c.description,
            created_at=c.created_at,
            relevance=5,  # пока константа, фронту достаточно
        )
        for c in complaints_sorted
    ]


# ======== 3) история сообщений (заглушка для Chat) ========

@router.get("/tickets/{ticket_id}/messages", response_model=list[MessageRead])
async def get_ticket_messages(ticket_id: int):
    """
    Пока возвращаем пустой список, чтобы фронт не падал.
    Можно позже прикрутить реальную историю сообщений.
    """
    return []


@router.post(
    "/tickets/{ticket_id}/messages",
    response_model=MessageRead,
)
async def add_ticket_message(ticket_id: int, payload: MessageCreate):
    """
    Заглушка на запись сообщения. 
    Сейчас ничего не сохраняем, просто эхо-ответ.
    """
    return MessageRead(
        id=None,
        role=payload.role,
        content=payload.content,
        created_at=datetime.utcnow(),
    )


# ======== 4) WebSocket для чата (заглушка) ========

@router.websocket("/ws/tickets/{ticket_id}")
async def tickets_ws(websocket: WebSocket, ticket_id: int, token: str | None = None):
    """
    Простая заглушка WS:
    - принимает одно сообщение от клиента
    - отвечает статическим текстом ассистента
    - закрывает соединение
    """
    await websocket.accept()

    try:
        while True:
            _ = await websocket.receive_text()
            await websocket.send_json(
                {
                    "role": "assistant",
                    "delta": "Пока стрим-чат не реализован на бэке 🙂",
                }
            )
            await websocket.close()
            break
    except WebSocketDisconnect:
        # клиент отключился — просто выходим
        pass
