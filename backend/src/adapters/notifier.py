from src.protocols.notifier import NotifierProtocol


class DummyNotifier(NotifierProtocol):
    async def notify_blocked_complaint(self, complaint_id: int, reason: str) -> None:
        # MVP-заглушка: просто лог/print; потом заменишь на реальный WS/Redis pub/sub/etc.
        print(f"[BLOCKED] complaint_id={complaint_id} reason={reason}")
