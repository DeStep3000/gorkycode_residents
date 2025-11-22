# app/adapters/repositories.py
from datetime import datetime
from typing import List, Optional, Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Executor, Complaint, Moderator, TicketStatus


class ExecutorRepositoryProtocol(Protocol):
    async def create_executor(
        self,
        session: AsyncSession,
        name: str,
        organization: Optional[str],
        phone: Optional[str],
        email: Optional[str],
    ) -> Executor: ...

    async def get_executor(
        self, session: AsyncSession, executor_id: int
    ) -> Optional[Executor]: ...

    async def get_executor_by_name(
        self, session: AsyncSession, name: str
    ) -> Optional[Executor]: ...

    async def update_executor(
        self,
        session: AsyncSession,
        executor_id: int,
        name: Optional[str],
        organization: Optional[str],
        phone: Optional[str],
        email: Optional[str],
    ) -> Executor: ...

    async def delete_executor(
        self, session: AsyncSession, executor_id: int
    ) -> None: ...


class ComplaintRepositoryProtocol(Protocol):
    async def create_complaint(
        self,
        session: AsyncSession,
        description: str,
        district: Optional[str],
        status: str,
        executor_id: Optional[int],
        address: str,
    ) -> Complaint: ...

    async def get_complaint(
        self, session: AsyncSession, complaint_id: int
    ) -> Optional[Complaint]: ...

    async def list_complaints(
        self, session: AsyncSession, limit: int = 50, offset: int = 0
    ) -> List[Complaint]: ...

    async def update_complaint(
        self,
        session: AsyncSession,
        complaint_id: int,
        status: Optional[str],
        resolution: Optional[str],
        executor_id: Optional[int],
        address: Optional[str],
    ) -> Complaint: ...

    async def delete_complaint(
        self, session: AsyncSession, complaint_id: int
    ) -> None: ...


class ModeratorRepositoryProtocol(Protocol):
    async def create_moderator(
        self,
        session: AsyncSession,
        username: str,
        full_name: str,
        email: Optional[str],
        phone: Optional[str],
    ) -> Moderator: ...

    async def get_moderator(
        self, session: AsyncSession, moderator_id: int
    ) -> Optional[Moderator]: ...

    async def update_moderator(
        self,
        session: AsyncSession,
        moderator_id: int,
        username: Optional[str],
        full_name: Optional[str],
        email: Optional[str],
        phone: Optional[str],
    ) -> Moderator: ...

    async def delete_moderator(
        self, session: AsyncSession, moderator_id: int
    ) -> None: ...


class TicketStatusRepositoryProtocol(Protocol):
    async def create_ticket_status(
        self,
        session: AsyncSession,
        complaint_id: int,
        status_code: str,
        sort_order: int,
        description: Optional[str],
        executor_id: Optional[int],
    ) -> TicketStatus: ...

    async def get_ticket_status(
        self, session: AsyncSession, complaint_id: int, status_code: str, data: datetime
    ) -> Optional[TicketStatus]: ...

    async def update_ticket_status(
        self,
        session: AsyncSession,
        complaint_id: int,
        status_code: str,
        description: Optional[str],
        sort_order: int,
        executor_id: Optional[int],
    ) -> TicketStatus: ...

    async def delete_ticket_status(
        self, session: AsyncSession, complaint_id: int, status_code: str, data: datetime
    ) -> None: ...
