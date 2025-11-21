from typing import Protocol, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Complaint, ComplaintHistory


class ComplaintRepositoryProtocol(Protocol):
    async def create_complaint(
        self,
        session: AsyncSession,
        *,
        description: str,
        district: str | None,
        executor_id: str | None,
    ) -> Complaint: ...

    async def get_complaint(
        self, session: AsyncSession, complaint_id: int
    ) -> Optional[Complaint]: ...

    async def list_complaints(
        self, session: AsyncSession, limit: int = 50, offset: int = 0
    ) -> tuple[List[Complaint], int]: ...

    async def update_complaint(
        self, session: AsyncSession, complaint: Complaint
    ) -> Complaint: ...


class ComplaintHistoryRepositoryProtocol(Protocol):
    async def get_or_create_history(
        self, session: AsyncSession, complaint_id: int
    ) -> ComplaintHistory: ...

    async def update_history(
        self,
        session: AsyncSession,
        history: ComplaintHistory,
    ) -> ComplaintHistory: ...
