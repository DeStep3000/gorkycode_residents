from src.schemas.executor_update import ExecutorUpdateRequest, ExecutorUpdateResult
from src.protocols.ai import AIClientProtocol


class DummyAIClient(AIClientProtocol):
    """
    MVP-заглушка: имитация ИИ.
    В реале – HTTP-клиент к внешнему сервису.
    """

    async def analyze_executor_response(
        self,
        *,
        complaint_description: str,
        update: ExecutorUpdateRequest,
    ) -> ExecutorUpdateResult:
        text = update.response_text.lower()

        # Очень грубая логика для MVP:
        # 1. если есть «перенаправить в ... <id>» — считаем, что есть целевой исполнитель
        target_executor_id = None
        is_forward = False
        is_blocking_bounce = False

        if "перенаправить" in text and "исполнителю" in text:
            # тут можно парсить id, пока просто заглушка
            target_executor_id = "parsed_executor_id"
            is_forward = True
        elif "это не наша зона" in text or "обратитесь в" in text:
            # явный отфутбол
            is_blocking_bounce = True

        return ExecutorUpdateResult(
            is_forward=is_forward,
            target_executor_id=target_executor_id,
            is_blocking_bounce=is_blocking_bounce,
            notes=None,
        )
