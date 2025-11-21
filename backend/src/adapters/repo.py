from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Complaint, ComplaintHistory, ComplaintStatus
from src.protocols.repo import (
    ComplaintRepositoryProtocol,
    ComplaintHistoryRepositoryProtocol,
)


class ComplaintRepository(ComplaintRepositoryProtocol):
    async def create_complaint(
        self,
        session: AsyncSession,
        *,
        description: str,
        district: str | None,
        executor_id: str | None,
    ) -> Complaint:
        complaint = Complaint(
            description=description,
            district=district,
            executor_id=executor_id,
            status=ComplaintStatus.NEW.value,
        )
        session.add(complaint)
        await session.flush()
        return complaint

    async def get_complaint(
        self, session: AsyncSession, complaint_id: int
    ) -> Optional[Complaint]:
        stmt = select(Complaint).where(Complaint.complaint_id == complaint_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_complaints(
        self,
        session: AsyncSession,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Complaint], int]:
        stmt = (
            select(Complaint)
            .order_by(Complaint.complaint_id)
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(stmt)
        items = result.scalars().all()

        total_stmt = select(func.count(Complaint.complaint_id))
        total = (await session.execute(total_stmt)).scalar_one()
        return items, total

    async def update_complaint(
        self, session: AsyncSession, complaint: Complaint
    ) -> Complaint:
        session.add(complaint)
        await session.flush()
        return complaint


class ComplaintHistoryRepository(ComplaintHistoryRepositoryProtocol):
    async def get_or_create_history(
        self, session: AsyncSession, complaint_id: int
    ) -> ComplaintHistory:
        stmt = select(ComplaintHistory).where(
            ComplaintHistory.complaint_id == complaint_id
        )
        result = await session.execute(stmt)
        history = result.scalar_one_or_none()
        if history is None:
            history = ComplaintHistory(
                complaint_id=complaint_id, executors_ids=[], responses={}
            )
            session.add(history)
            await session.flush()
        return history

    async def update_history(
        self,
        session: AsyncSession,
        history: ComplaintHistory,
    ) -> ComplaintHistory:
        session.add(history)
        await session.flush()
        return history
