from typing import Protocol

from src.schemas.executor_update import ExecutorUpdateRequest, ExecutorUpdateResult


class AIClientProtocol(Protocol):
    async def analyze_executor_response(
        self,
        *,
        complaint_description: str,
        update: ExecutorUpdateRequest,
    ) -> ExecutorUpdateResult: ...
