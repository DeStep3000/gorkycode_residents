# src/adapters/ai.py
from __future__ import annotations

import json
import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from src.protocols.ai import AIClientProtocol
from src.schemas.executor_update import (ExecutorUpdateRequest,
                                         ExecutorUpdateResult)

# Загружаем переменные окружения из .env (локальная разработка)
load_dotenv()

YC_FOLDER_ID = os.getenv("YC_FOLDER_ID")
YC_API_KEY = os.getenv("YC_API_KEY")
YC_MODEL = os.getenv("YC_MODEL", "yandexgpt-lite/rc")


# ==========================
#  PROMPT для YandexGPT
# ==========================

EXECUTOR_RESPONSE_SYSTEM_PROMPT = """
Ты — интеллектуальный помощник модератора платформы «Лобачевский».
Твоя задача — анализировать текст ответа исполнителя на жалобу жителя
и классифицировать его по признакам «футбола».

Входные данные:
- complaint_description — текст жалобы жителя (может содержать служебную информацию о времени)
- executor_response — текст ответа исполнителя по этой жалобе

Нужно определить:

1) is_forward:
   Является ли ответ фактическим перенаправлением жалобы на другого исполнителя
   или организацию.

   Примеры перенаправления:
   - «Просьба перенаправить в ДУК Приокского района»
   - «Обратитесь в ГИБДД»
   - «Заявка передана в регионального оператора ООО “Нижэкология-НН”»
   - «заявка передана в управляющую компанию» и т.п.

2) target_executor_name:
   Кому именно предлагается обратиться или куда перенаправлена заявка.
   Это может быть конкретная организация, служба или тип исполнителя:
   - «ДУК Приокского района»
   - «ГИБДД»
   - «региональный оператор по вывозу мусора»
   - «управляющая компания»
   Если в ответе явно нет понятного адресата — оставить null.

3) is_blocking_bounce:
   Является ли ответ «плохим футболом»:
   - исполнитель отказывает в решении проблемы
   - не берёт на себя ответственность
   - и НЕ даёт понятного адресата, куда нужно обратиться

   Примеры «плохого футбола»:
   - «не наша компетенция», «не относится к нашим полномочиям»
   - «мы этим не занимаемся»
   - общие фразы типа «обратитесь в соответствующую организацию»
     без указания конкретной организации или службы.

4) notes:
   Краткое пояснение для модератора, что произошло и почему так классифицировано.

Формат ответа — строго JSON без лишнего текста:

{
  "is_forward": true/false,
  "target_executor_name": "строка или null",
  "is_blocking_bounce": true/false,
  "notes": "краткое пояснение на русском языке"
}

Правила:

- Если по смыслу ответ: «работа выполнена», «устранено», «меры приняты»,
  без просьбы обратиться куда-то ещё, то:
  - is_forward = false
  - target_executor_name = null
  - is_blocking_bounce = false

- Если есть явные формулировки:
  - «просим перенаправить в ...»
  - «обратитесь в ...»
  - «заявка передана в ...»
  - «компетенция такой-то организации»
  то:
  - is_forward = true
  - target_executor_name = извлечённое название организации или типа исполнителя

- Если есть отказ («не наша компетенция», «не относимся», «мы этим не занимаемся»)
  и при этом нет понятного адресата, то:
  - is_blocking_bounce = true
  - target_executor_name = null (если его нельзя однозначно определить)
""".strip()



class YandexAIClient(AIClientProtocol):
    """
    Реальный клиент ИИ: ходит в YandexGPT через OpenAI-совместимый API.
    Для работы нужны переменные окружения:
      - YC_FOLDER_ID
      - YC_API_KEY
      - (опционально) YC_MODEL
    """

    def __init__(self) -> None:
        if not YC_FOLDER_ID or not YC_API_KEY:
            raise RuntimeError(
                "YandexAIClient: YC_FOLDER_ID и YC_API_KEY должны быть заданы "
                "в переменных окружения или в .env"
            )

        self._client = OpenAI(
            api_key=YC_API_KEY,
            base_url="https://rest-assistant.api.cloud.yandex.net/v1",
            project=YC_FOLDER_ID,
        )

    async def analyze_executor_response(
        self,
        *,
        complaint_description: str,
        update: ExecutorUpdateRequest,
    ) -> ExecutorUpdateResult:
        """
        Отправляем в модель JSON с описанием жалобы и ответом исполнителя.
        Модель отвечает JSON с флагами is_forward / is_blocking_bounce и
        именем целевого исполнителя.
        """

        payload = {
            "complaint_description": complaint_description,
            "executor_response": update.response_text,
            # при желании сюда можно добавлять служебные поля по времени:
            # "status": update.status,
            # "executed_at": update.executed_at.isoformat() if update.executed_at else None,
        }

        response = self._client.responses.create(
            model=f"gpt://{YC_FOLDER_ID}/{YC_MODEL}",
            temperature=0.1,
            instructions=EXECUTOR_RESPONSE_SYSTEM_PROMPT,
            input=json.dumps(payload, ensure_ascii=False),
            max_output_tokens=400,
        )

        # Модель по инструкции должна вернуть чистый JSON
        raw = response.output_text
        data = json.loads(raw)

        is_forward = bool(data.get("is_forward"))
        is_blocking_bounce = bool(data.get("is_blocking_bounce"))
        target_executor_name = data.get("target_executor_name")
        notes = data.get("notes")

        # Здесь можно привязать имя исполнителя к ID из вашей БД.
        # Пока что оставляем target_executor_id = None,
        # а дальнейший маппинг можно сделать в сервисе.
        target_executor_id: Optional[str] = None

        return ExecutorUpdateResult(
            is_forward=is_forward,
            target_executor_id=target_executor_id,
            is_blocking_bounce=is_blocking_bounce,
            notes=notes,
        )
