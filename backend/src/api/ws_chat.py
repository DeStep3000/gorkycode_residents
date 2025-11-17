from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from dishka.integrations.fastapi import inject, FromDishka
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

from src.core.config import settings
from src.services.chat import ChatService

router = APIRouter(prefix="/ws", tags=["ws"])
ws_bearer = HTTPBearer(auto_error=False)


async def get_user_id_from_token(token: str) -> int:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    sub = payload.get("sub")
    return int(sub)


@router.websocket("/tickets/{ticket_id}")
@inject
async def ticket_chat_ws(
    websocket: WebSocket,
    ticket_id: int,
    chat_service: FromDishka[ChatService],
    token: str = Query(...),  # фронт шлёт ?token=...
):
    try:
        user_id = await get_user_id_from_token(token)
    except (JWTError, TypeError, ValueError):
        await websocket.close(code=4401)
        return

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            async for chunk in chat_service.stream_ai_answer(
                ticket_id=ticket_id,
                sender_id=user_id,
                user_message=data,
            ):
                await websocket.send_json({"role": "assistant", "delta": chunk})
    except WebSocketDisconnect:
        return
