from __future__ import annotations

import json
import os
import re
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from src.protocols.ai import AIClientProtocol
from src.schemas.executor_update import ExecutorUpdateRequest, ExecutorUpdateResult

# Загружаем переменные окружения из .env (локальная разработка)
load_dotenv()

YC_FOLDER_ID = os.getenv("YC_FOLDER_ID")
YC_API_KEY = os.getenv("YC_API_KEY")
YC_MODEL = os.getenv("YC_MODEL", "yandexgpt-lite/rc")


# ==========================
#  PROMPT для YandexGPT
#  (та же логика, что в тестовом скрипте, но без эскалации)
# ==========================

EXECUTOR_RESPONSE_SYSTEM_PROMPT = """
Ты — интеллектуальный помощник модератора платформы «Лобачевский».

Твоя задача:
проанализировать одну конкретную заявку по структурированным данным,
учитывая текст жалобы, текст ответа исполнителя и длительность рассмотрения,
и вернуть РЕШЕНИЕ ДЛЯ МОДЕРАТОРА.

Тебе передают JSON такого вида:

{
  "complaint_id": int,
  "status": "текущий статус в системе",
  "district": int | null,
  "executor_id": int | null,

  "texts": {
    "description": "текст жалобы жителя",
    "executor_response": "текст служебного ответа исполнителя (резолюция)"
  },

  "timing": {
    "real_duration_days": float | null,
    "expected_duration_days": float | null,
    "delay_days": float | null,
    "football_threshold_days": float | null,
    "ratio_to_expected": float | null
  }
}

Нужно ВЕРНУТЬ JSON СТРОГО следующего вида:

{
  "decision": "forward" | "stop" | "ok",
  "is_forward": true/false,
  "is_blocking_bounce": true/false,
  "target_executor_name": "строка или null",
  "moderator_message": "короткое пояснение для модератора",
  "ai_badge": "Перенаправлена ИИ" | "Остановлена ИИ" | "Без вмешательства ИИ"
}

ОПИСАНИЕ ПОЛЕЙ:

1) decision:
   - "forward" — ответ исполнителя явно перекладывает ответственность на другого исполнителя или организацию.
   - "stop" — плохой футбол: исполнитель отказывается, снимает с себя ответственность и НЕ указывает конкретного адресата.
   - "ok" — футбол отсутствует, исполнитель работает по заявке, ответ по существу.

2) is_forward:
   true — если по тексту executor_response видно, что заявка должна уйти другому исполнителю
   (например: «перенаправить в …», «заявка передана …», «обратитесь в ГИБДД»).

3) target_executor_name:
   Название новой организации/исполнителя.
   Если определить невозможно — null.

4) is_blocking_bounce:
   true — если это «плохой футбол»:
   - «не наша компетенция», «не относимся», «мы этим не занимаемся»,
   - «обратитесь в соответствующую организацию» без указания, в какую именно.

5) moderator_message:
   Короткое пояснение:
   - что сделал исполнитель (выполнил / перекинул / отказался),
   - кому нужно переназначить (если decision="forward"),
   - учти длительность, если real_duration_days заметно превышает expected_duration_days
     или football_threshold_days — упомяни это.

6) ai_badge:
   - "Перенаправлена ИИ"  — если decision="forward"
   - "Остановлена ИИ"     — если decision="stop"
   - "Без вмешательства ИИ" — если decision="ok"

ВРЕМЯ:
- Время влияет только на формулировку moderator_message.
- Никаких дополнительных статусов на основе времени нет.
- Даже если заявка “долго висит”, решение остаётся только из трёх:
  forward / stop / ok.

Формат ответа:
- Строго один JSON-объект.
- Никакого Markdown, без ```json, без текста до или после.
""".strip()


def _extract_json_maybe(text: str) -> dict:
    """
    Аккуратно вытаскиваем JSON из ответа модели.
    Иногда YandexGPT может добавить лишние символы/текст вокруг.
    """
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError(
            f"JSON не найден в тексте ответа модели:\n{text[:200]}...")
    candidate = match.group(0)
    return json.loads(candidate)


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
        Формируем структурированный payload (как в тесте) и отправляем в модель.
        Модель отвечает JSON со структурой:
          decision, is_forward, is_blocking_bounce, target_executor_name,
          moderator_message, ai_badge.
        Мы маппим это на ExecutorUpdateResult.
        """

        # Пытаемся аккуратно вытащить максимум полей из update.
        # Если каких-то атрибутов нет в ExecutorUpdateRequest — будет None, всё ок.
        complaint_id = getattr(update, "complaint_id", None)
        status = getattr(update, "status", None)
        district = getattr(update, "district", None)
        executor_id = getattr(update, "executor_id", None)

        real_duration_days = getattr(update, "real_duration_days", None)
        expected_duration_days = getattr(
            update, "expected_duration_days", None)
        delay_days = getattr(update, "delay_days", None)
        football_threshold_days = getattr(
            update, "football_threshold_days", None)
        ratio_to_expected = getattr(update, "ratio_to_expected", None)

        timing = {
            "real_duration_days": float(real_duration_days) if real_duration_days is not None else None,
            "expected_duration_days": float(expected_duration_days) if expected_duration_days is not None else None,
            "delay_days": float(delay_days) if delay_days is not None else None,
            "football_threshold_days": float(football_threshold_days) if football_threshold_days is not None else None,
            "ratio_to_expected": float(ratio_to_expected) if ratio_to_expected is not None else None,
        }

        payload = {
            "complaint_id": int(complaint_id) if complaint_id is not None else None,
            "status": status,
            "district": int(district) if district is not None else None,
            "executor_id": int(executor_id) if executor_id is not None else None,
            "texts": {
                "description": complaint_description,
                "executor_response": update.response_text,
            },
            "timing": timing,
        }

        response = self._client.responses.create(
            model=f"gpt://{YC_FOLDER_ID}/{YC_MODEL}",
            temperature=0.1,
            instructions=EXECUTOR_RESPONSE_SYSTEM_PROMPT,
            input=json.dumps(payload, ensure_ascii=False),
            max_output_tokens=400,
        )

        raw = response.output_text

        # Страхуемся от лишнего текста вокруг JSON
        data = _extract_json_maybe(raw)

        # Шесть полей из ответа модели
        decision = data.get("decision")
        is_forward = bool(data.get("is_forward"))
        is_blocking_bounce = bool(data.get("is_blocking_bounce"))
        target_executor_name: Optional[str] = data.get("target_executor_name")
        moderator_message: Optional[str] = data.get("moderator_message")
        ai_badge: Optional[str] = data.get("ai_badge")

        return ExecutorUpdateResult(
            decision=decision,
            is_forward=is_forward,
            is_blocking_bounce=is_blocking_bounce,
            target_executor_name=target_executor_name,
            moderator_message=moderator_message,
            ai_badge=ai_badge,
        )
