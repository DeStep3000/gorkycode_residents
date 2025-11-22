# app/adapters/repositories.py
from datetime import datetime
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.db.models import Executor, Complaint, Moderator, TicketStatus
from src.protocols.repo import (
    ExecutorRepositoryProtocol,
    ComplaintRepositoryProtocol,
    ModeratorRepositoryProtocol,
    TicketStatusRepositoryProtocol,
)


class ExecutorRepository(ExecutorRepositoryProtocol):
    async def create_executor(
        self,
        session: AsyncSession,
        name: str,
        organization: Optional[str],
        phone: Optional[str],
        email: Optional[str],
    ) -> Executor:
        executor = Executor(
            name=name, organization=organization, phone=phone, email=email
        )
        session.add(executor)
        await session.flush()
        return executor

    async def get_executor(
        self, session: AsyncSession, executor_id: int
    ) -> Optional[Executor]:
        stmt = select(Executor).filter(Executor.executor_id == executor_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get_executor_by_name(
        self, session: AsyncSession, name: str
    ) -> Optional[Executor]:
        stmt = select(Executor).filter(Executor.name == name)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def update_executor(
        self,
        session: AsyncSession,
        executor_id: int,
        name: Optional[str],
        organization: Optional[str],
        phone: Optional[str],
        email: Optional[str],
    ) -> Executor:
        executor = await self.get_executor(session, executor_id)
        if executor:
            if name is not None:
                executor.name = name
            if organization is not None:
                executor.organization = organization
            if phone is not None:
                executor.phone = phone
            if email is not None:
                executor.email = email
            session.add(executor)
            await session.flush()
            return executor
        raise ValueError("Executor not found")

    async def delete_executor(self, session: AsyncSession, executor_id: int) -> None:
        executor = await self.get_executor(session, executor_id)
        if executor:
            await session.delete(executor)
            await session.flush()


class ComplaintRepository(ComplaintRepositoryProtocol):
    async def create_complaint(
        self,
        session: AsyncSession,
        description: str,
        district: Optional[str],
        status: str,
        executor_id: Optional[int],
        address: str,
    ) -> Complaint:
        complaint = Complaint(
            description=description,
            district=district,
            status=status,
            executor_id=executor_id,
            address=address,
        )
        session.add(complaint)
        await session.flush()
        return complaint

    async def get_complaint(
        self, session: AsyncSession, complaint_id: int
    ) -> Optional[Complaint]:
        stmt = select(Complaint).filter(Complaint.complaint_id == complaint_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def list_complaints(
        self, session: AsyncSession, limit: int = 50, offset: int = 0
    ) -> List[Complaint]:
        stmt = select(Complaint).limit(limit).offset(offset)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def update_complaint(
        self,
        session: AsyncSession,
        complaint_id: int,
        status: Optional[str],
        resolution: Optional[str],
        executor_id: Optional[int],
        address: Optional[str],
    ) -> Complaint:
        complaint = await self.get_complaint(session, complaint_id)
        if complaint:
            if status is not None:
                complaint.status = status
            if resolution is not None:
                complaint.resolution = resolution
            if executor_id is not None:
                complaint.executor_id = executor_id
            if address is not None:
                complaint.address = address
            session.add(complaint)
            await session.flush()
            return complaint
        raise ValueError("Complaint not found")

    async def delete_complaint(self, session: AsyncSession, complaint_id: int) -> None:
        complaint = await self.get_complaint(session, complaint_id)
        if complaint:
            await session.delete(complaint)
            await session.flush()


class ModeratorRepository(ModeratorRepositoryProtocol):
    async def create_moderator(
        self,
        session: AsyncSession,
        username: str,
        full_name: str,
        email: Optional[str],
        phone: Optional[str],
    ) -> Moderator:
        moderator = Moderator(
            username=username, full_name=full_name, email=email, phone=phone
        )
        session.add(moderator)
        await session.flush()
        return moderator

    async def get_moderator(
        self, session: AsyncSession, moderator_id: int
    ) -> Optional[Moderator]:
        stmt = select(Moderator).filter(Moderator.moderator_id == moderator_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def update_moderator(
        self,
        session: AsyncSession,
        moderator_id: int,
        username: Optional[str],
        full_name: Optional[str],
        email: Optional[str],
        phone: Optional[str],
    ) -> Moderator:
        moderator = await self.get_moderator(session, moderator_id)
        if moderator:
            if username is not None:
                moderator.username = username
            if full_name is not None:
                moderator.full_name = full_name
            if email is not None:
                moderator.email = email
            if phone is not None:
                moderator.phone = phone
            session.add(moderator)
            await session.flush()
            return moderator
        raise ValueError("Moderator not found")

    async def delete_moderator(self, session: AsyncSession, moderator_id: int) -> None:
        moderator = await self.get_moderator(session, moderator_id)
        if moderator:
            await session.delete(moderator)
            await session.flush()


class TicketStatusRepository(TicketStatusRepositoryProtocol):
    async def create_ticket_status(
        self,
        session: AsyncSession,
        complaint_id: int,
        status_code: str,
        sort_order: int,
        description: Optional[str],
        executor_id: Optional[int],
    ) -> TicketStatus:
        ticket_status = TicketStatus(
            complaint_id=complaint_id,
            status_code=status_code,
            sort_order=sort_order,
            description=description,
            executor_id=executor_id,
        )
        session.add(ticket_status)
        await session.flush()
        return ticket_status

    async def get_ticket_status(
        self, session: AsyncSession, complaint_id: int, status_code: str, data: datetime
    ) -> Optional[TicketStatus]:
        stmt = select(TicketStatus).filter(
            TicketStatus.complaint_id == complaint_id,
            TicketStatus.status_code == status_code,
            TicketStatus.data == data,
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    async def update_ticket_status(
        self,
        session: AsyncSession,
        complaint_id: int,
        status_code: str,
        description: Optional[str],
        sort_order: int,
        executor_id: Optional[int],
    ) -> TicketStatus:
        ticket_status = await self.get_ticket_status(
            session, complaint_id, status_code, datetime.utcnow()
        )
        if ticket_status:
            if description is not None:
                ticket_status.description = description
            if sort_order is not None:
                ticket_status.sort_order = sort_order
            if executor_id is not None:
                ticket_status.executor_id = executor_id
            session.add(ticket_status)
            await session.flush()
            return ticket_status
        raise ValueError("TicketStatus not found")

    async def delete_ticket_status(
        self, session: AsyncSession, complaint_id: int, status_code: str, data: datetime
    ) -> None:
        ticket_status = await self.get_ticket_status(
            session, complaint_id, status_code, data
        )
        if ticket_status:
            await session.delete(ticket_status)
            await session.flush()
