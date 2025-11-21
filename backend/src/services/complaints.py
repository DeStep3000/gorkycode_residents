# app/services/complaints.py
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.protocols.repo import (
    ComplaintRepositoryProtocol,
    ComplaintHistoryRepositoryProtocol,
)
from src.protocols.ai import AIClientProtocol
from src.protocols.notifier import NotifierProtocol
from src.db.models import ComplaintStatus
from src.schemas.complaint import ComplaintCreate, ComplaintUpdate
from src.schemas.executor_update import ExecutorUpdateRequest


class ComplaintService:
    def __init__(
        self,
        complaint_repo: ComplaintRepositoryProtocol,
        history_repo: ComplaintHistoryRepositoryProtocol,
        ai_client: AIClientProtocol,
        notifier: NotifierProtocol,
    ):
        self._complaint_repo = complaint_repo
        self._history_repo = history_repo
        self._ai_client = ai_client
        self._notifier = notifier

    async def create_complaint(
        self,
        session: AsyncSession,
        data: ComplaintCreate,
    ):
        complaint = await self._complaint_repo.create_complaint(
            session,
            description=data.description,
            district=data.district,
            executor_id=data.executor_id,
        )
        # создаём пустую историю
        await self._history_repo.get_or_create_history(session, complaint.complaint_id)
        await session.commit()
        await session.refresh(complaint)
        return complaint

    async def get_complaint(self, session: AsyncSession, complaint_id: int):
        return await self._complaint_repo.get_complaint(session, complaint_id)

    async def list_complaints(
        self, session: AsyncSession, limit: int = 50, offset: int = 0
    ):
        return await self._complaint_repo.list_complaints(
            session, limit=limit, offset=offset
        )

    async def update_complaint(
        self,
        session: AsyncSession,
        complaint_id: int,
        data: ComplaintUpdate,
    ):
        complaint = await self._complaint_repo.get_complaint(session, complaint_id)
        if complaint is None:
            return None

        if data.status is not None:
            complaint.status = data.status.value
        if data.resolution is not None:
            complaint.resolution = data.resolution
        if data.executor_id is not None:
            complaint.executor_id = data.executor_id
        if data.execution_date is not None:
            complaint.execution_date = data.execution_date
        if data.final_status_at is not None:
            complaint.final_status_at = data.final_status_at

        await self._complaint_repo.update_complaint(session, complaint)
        await session.commit()
        await session.refresh(complaint)
        return complaint

    async def get_history(self, session: AsyncSession, complaint_id: int):
        history = await self._history_repo.get_or_create_history(session, complaint_id)
        await session.commit()
        await session.refresh(history)
        return history

    async def handle_executor_update(
        self,
        session: AsyncSession,
        complaint_id: int,
        update: ExecutorUpdateRequest,
    ):
        complaint = await self._complaint_repo.get_complaint(session, complaint_id)
        if complaint is None:
            return None

        history = await self._history_repo.get_or_create_history(session, complaint_id)

        # Обновляем историю
        if update.executor_id not in history.executors_ids:
            history.executors_ids.append(update.executor_id)

        history.responses.setdefault(update.executor_id, {})
        history.responses[update.executor_id] = {
            "response": update.response_text,
            "status": update.status,
            "executed_at": (update.executed_at or datetime.utcnow()).isoformat(),
        }

        await self._history_repo.update_history(session, history)

        # Запускаем ИИ-анализ
        ai_result = await self._ai_client.analyze_executor_response(
            complaint_description=complaint.description,
            update=update,
        )

        # 1. Если понятно, кому перенаправить – переназначаем исполнителя и ставим статус REDIRECTED
        if ai_result.is_forward and ai_result.target_executor_id:
            complaint.executor_id = ai_result.target_executor_id
            complaint.status = ComplaintStatus.REDIRECTED.value

        # 2. Ясно, что заявку отфутболили, но непонятно куда – блокируем, уведомляем админку
        elif ai_result.is_blocking_bounce:
            complaint.status = ComplaintStatus.BLOCKED.value
            complaint.final_status_at = datetime.utcnow()
            await self._notifier.notify_blocked_complaint(
                complaint_id=complaint.complaint_id,
                reason=ai_result.notes or "executor bounced request without target",
            )

        # 3. Обычная заявка – просто обновляем финальное состояние
        else:
            complaint.resolution = update.response_text
            if update.executed_at:
                complaint.execution_date = update.executed_at
            complaint.status = (
                ComplaintStatus.IN_PROGRESS.value
                if (update.status or "").lower() != "done"
                else ComplaintStatus.COMPLETED.value
            )
            if complaint.status == ComplaintStatus.COMPLETED.value:
                complaint.final_status_at = datetime.utcnow()

        await self._complaint_repo.update_complaint(session, complaint)
        await session.commit()
        await session.refresh(complaint)
        return complaint
