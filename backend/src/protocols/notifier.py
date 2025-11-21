from typing import Protocol


class NotifierProtocol(Protocol):
    async def notify_blocked_complaint(
        self, complaint_id: int, reason: str
    ) -> None: ...
