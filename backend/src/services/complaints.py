# app/services/complaints.py
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.repo import (
    ComplaintRepositoryProtocol,
    ExecutorRepositoryProtocol,
    ModeratorRepositoryProtocol,
    TicketStatusRepositoryProtocol,
)
from src.adapters.ai import AIClientProtocol
from src.api.ws import send_notification_to_clients
from src.schemas.complaint import ComplaintStatus
from src.schemas.executor_update import ExecutorUpdateRequest


class ComplaintService:
    def __init__(
        self,
        complaint_repo: ComplaintRepositoryProtocol,
        executor_repo: ExecutorRepositoryProtocol,
        moderator_repo: ModeratorRepositoryProtocol,
        ticket_status_repo: TicketStatusRepositoryProtocol,
        ai_client: AIClientProtocol,
    ):
        self._complaint_repo = complaint_repo
        self._executor_repo = executor_repo
        self._moderator_repo = moderator_repo
        self._ticket_status_repo = ticket_status_repo
        self._ai_client = ai_client

    # ============================
    # CRUD для Complaint
    # ============================

    async def create_complaint(
        self,
        session: AsyncSession,
        description: str,
        district: Optional[str] = None,
        status: ComplaintStatus = ComplaintStatus.NEW,
        executor_id: Optional[int] = None,
        address: str = "",
    ):
        complaint = await self._complaint_repo.create_complaint(
            session,
            description=description,
            district=district,
            status=status.value,  # Преобразуем статус в строку
            executor_id=executor_id,
            address=address,
        )
        # Создаем начальный статус для заявки
        await self._ticket_status_repo.create_ticket_status(
            session,
            complaint_id=complaint.complaint_id,
            status_code=status.value,
            sort_order=1,
            description="Заявка создана",
            executor_id=executor_id,
        )

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
        status: Optional[ComplaintStatus] = None,
        resolution: Optional[str] = None,
        executor_id: Optional[int] = None,
        address: Optional[str] = None,
    ):
        complaint = await self._complaint_repo.get_complaint(session, complaint_id)
        if complaint is None:
            return None

        # Обновляем поля
        if status is not None:
            complaint.status = status.value
        if resolution is not None:
            complaint.resolution = resolution
        if executor_id is not None:
            complaint.executor_id = executor_id
        if address is not None:
            complaint.address = address

        await self._complaint_repo.update_complaint(session, complaint)
        await session.commit()
        await session.refresh(complaint)

        if status is not None:
            # Обновляем статус в TicketStatus
            await self._ticket_status_repo.create_ticket_status(
                session,
                complaint_id=complaint_id,
                status_code=status.value if status else complaint.status,
                sort_order=2,  # следующий статус
                description=resolution if resolution else "Обновлено",
                executor_id=executor_id,
            )

        return complaint

    async def delete_complaint(self, session: AsyncSession, complaint_id: int):
        await self._complaint_repo.delete_complaint(session, complaint_id)

    # ============================
    # CRUD для Executor
    # ============================

    async def create_executor(
        self,
        session: AsyncSession,
        name: str,
        organization: Optional[str],
        phone: Optional[str],
        email: Optional[str],
    ):
        return await self._executor_repo.create_executor(
            session, name, organization, phone, email
        )

    async def get_executor(self, session: AsyncSession, executor_id: int):
        return await self._executor_repo.get_executor(session, executor_id)

    async def get_executor_by_name(
        self, session: AsyncSession, name: str
    ) -> Optional[ExecutorUpdateRequest]:
        executor = await self._executor_repo.get_executor_by_name(session, name)
        if not executor:
            return None
        return executor

    async def update_executor(
        self,
        session: AsyncSession,
        executor_id: int,
        name: Optional[str],
        organization: Optional[str],
        phone: Optional[str],
        email: Optional[str],
    ):
        return await self._executor_repo.update_executor(
            session, executor_id, name, organization, phone, email
        )

    async def delete_executor(self, session: AsyncSession, executor_id: int):
        await self._executor_repo.delete_executor(session, executor_id)

    # ============================
    # CRUD для Moderator
    # ============================

    async def create_moderator(
        self,
        session: AsyncSession,
        username: str,
        full_name: str,
        email: Optional[str],
        phone: Optional[str],
    ):
        return await self._moderator_repo.create_moderator(
            session, username, full_name, email, phone
        )

    async def get_moderator(self, session: AsyncSession, moderator_id: int):
        return await self._moderator_repo.get_moderator(session, moderator_id)

    async def update_moderator(
        self,
        session: AsyncSession,
        moderator_id: int,
        username: Optional[str],
        full_name: Optional[str],
        email: Optional[str],
        phone: Optional[str],
    ):
        return await self._moderator_repo.update_moderator(
            session, moderator_id, username, full_name, email, phone
        )

    async def delete_moderator(self, session: AsyncSession, moderator_id: int):
        await self._moderator_repo.delete_moderator(session, moderator_id)

    # ============================
    # Обработка запроса от Executor
    # ============================

    async def handle_executor_update(
        self,
        session: AsyncSession,
        complaint_id: int,
        update: ExecutorUpdateRequest,
    ):
        complaint = await self._complaint_repo.get_complaint(session, complaint_id)
        if complaint is None:
            return None

        # Запускаем анализ с помощью ИИ
        ai_result = await self._ai_client.analyze_executor_response(
            complaint_description=complaint.description,
            update=update,
        )

        ticket_statuses = await self._ticket_status_repo.get_ticket_status(session, complaint_id)

        # Логика перенаправления заявки или закрытия

        if ai_result.is_forward and ai_result.target_executor_name:
            # Перенаправляем заявку другому исполнителю
            ex_id = await self._executor_repo.get_executor_by_name(
                session, ai_result.target_executor_name
            )
            if ex_id:
                complaint.complaint_id = ex_id.executor_id

                flag=False
                for status in ticket_statuses:
                    if status.executor_id == update.executor_id:
                        flag=True

                if flag:
                    complaint.status = ComplaintStatus.BLOCK_WORKFLOW.value
                    complaint.final_status_at = datetime.utcnow()

                    await self._complaint_repo.update_complaint(session,
                                                                complaint.complaint_id,
                                                                complaint.status,
                                                                update.response_text,
                                                                complaint.executor_id,
                                                                complaint.address, )

                    await self._ticket_status_repo.create_ticket_status(
                        session,
                        complaint_id=complaint.complaint_id,
                        status_code=ComplaintStatus.BLOCK_WORKFLOW.value,
                        sort_order=2,  # следующий статус
                        description=update.response_text,
                        executor_id=complaint.executor_id,
                    )

                    notification_message = {
                        "complaint_id": complaint.complaint_id,
                        "type": "block",
                        "description": "Произошла блокировка",
                    }
                    await send_notification_to_clients(notification_message)

            else:
                complaint.status = ComplaintStatus.BLOCK_WORKFLOW.value
                complaint.final_status_at = datetime.utcnow()

                await self._complaint_repo.update_complaint(session,
                                                            complaint.complaint_id,
                                                            complaint.status,
                                                            update.response_text,
                                                            complaint.executor_id,
                                                            complaint.address, )

                await self._ticket_status_repo.create_ticket_status(
                    session,
                    complaint_id=complaint.complaint_id,
                    status_code=ComplaintStatus.BLOCK_WORKFLOW.value,
                    sort_order=2,  # следующий статус
                    description=update.response_text,
                    executor_id=complaint.executor_id,
                )

                notification_message = {
                    "complaint_id": complaint.complaint_id,
                    "type": "block",
                    "description": "Произошла блокировка",
                }
                await send_notification_to_clients(notification_message)


            complaint.status = ComplaintStatus.ASSIGNED_RESPONSIBLE.value

            await self._complaint_repo.update_complaint(session,
                                                        complaint.complaint_id,
                                                        complaint.status,
                                                        update.response_text,
                                                        complaint.executor_id,
                                                        complaint.address,)

            # Создаем новую запись в ticket_status
            await self._ticket_status_repo.create_ticket_status(
                session,
                complaint_id=complaint.complaint_id,
                status_code=ComplaintStatus.ASSIGNED_RESPONSIBLE.value,
                sort_order=2,  # следующий статус
                description=update.response_text,
                executor_id=complaint.executor_id,
            )

            notification_message = {
                "complaint_id": complaint.complaint_id,
                "type": "redirect",
                "description": "Перенаправили заявку другому исполнителю",
            }
            await send_notification_to_clients(notification_message)

        elif ai_result.is_blocking_bounce:
            # Если задача не может быть выполнена (отфутболена), блокируем заявку
            complaint.status = ComplaintStatus.BLOCK_WORKFLOW.value
            complaint.final_status_at = datetime.utcnow()

            await self._complaint_repo.update_complaint(session,
                                                        complaint.complaint_id,
                                                        complaint.status,
                                                        update.response_text,
                                                        complaint.executor_id,
                                                        complaint.address,)

            await self._ticket_status_repo.create_ticket_status(
                session,
                complaint_id=complaint.complaint_id,
                status_code=ComplaintStatus.BLOCK_WORKFLOW.value,
                sort_order=2,  # следующий статус
                description=update.response_text,
                executor_id=complaint.executor_id,
            )

            notification_message = {
                "complaint_id": complaint.complaint_id,
                "type": "block",
                "description": "Произошла блокировка",
            }
            await send_notification_to_clients(notification_message)

        else:
            # Если все хорошо, отправляем на статус "MODERATED"
            complaint.status = ComplaintStatus.MODERATED.value

            # Создаем новую запись в ticket_status
            await self._ticket_status_repo.create_ticket_status(
                session,
                complaint_id=complaint.complaint_id,
                status_code=ComplaintStatus.MODERATED.value,
                sort_order=2,  # следующий статус
                description=update.response_text,
                executor_id=complaint.executor_id,
            )

            await self._complaint_repo.update_complaint(session,
                                                        complaint.complaint_id,
                                                        complaint.status,
                                                        update.response_text,
                                                        complaint.executor_id,
                                                        complaint.address,)
        await session.commit()
        await session.refresh(complaint)

        return complaint

    # ============================
    # CRUD для TicketStatus
    # ============================

    async def create_ticket_status(
        self,
        session: AsyncSession,
        complaint_id: int,
        status_code: str,
        sort_order: int,
        description: Optional[str],
        executor_id: Optional[int],
    ):
        return await self._ticket_status_repo.create_ticket_status(
            session, complaint_id, status_code, sort_order, description, executor_id
        )

    async def get_ticket_status(
        self, session: AsyncSession, complaint_id: int
    ):
        return await self._ticket_status_repo.get_ticket_status(
            session, complaint_id
        )

    async def update_ticket_status(
        self,
        session: AsyncSession,
        complaint_id: int,
        status_code: str,
        description: Optional[str],
        sort_order: int,
        executor_id: Optional[int],
    ):
        return await self._ticket_status_repo.update_ticket_status(
            session, complaint_id, status_code, description, sort_order, executor_id
        )

    async def delete_ticket_status(
        self, session: AsyncSession, complaint_id: int, status_code: str, data: datetime
    ):
        await self._ticket_status_repo.delete_ticket_status(
            session, complaint_id, status_code, data
        )
