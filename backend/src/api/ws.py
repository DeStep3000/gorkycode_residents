# app/api/websocket_notifications.py
import json

from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import List
import asyncio

router = APIRouter()

# Список активных WebSocket-соединений
active_connections: List[WebSocket] = []

# Очередь для уведомлений
notification_queue = asyncio.Queue()

# Ручка WebSocket-соединения
@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Ждем сообщений от клиента (можно использовать для ping-pong или других задач)
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)


# Функция для отправки уведомлений на фронт
async def send_notification_to_clients(message: dict):
    # Преобразуем сообщение в JSON строку
    message_json =  json.dumps(message)
    for connection in active_connections:
        await connection.send_text(message)
