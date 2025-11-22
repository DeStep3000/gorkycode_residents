# app/api/v1/complaints.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from dishka.integrations.fastapi import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dto import ExecutorDTO, ComplaintDTO, ModeratorDTO
from src.db.session import get_session
from src.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ModeratorCreate,
    ModeratorUpdate,
)
from src.schemas.executor_update import ExecutorUpdateRequest
from src.services.complaints import ComplaintService

router = APIRouter()


SessionDep = Annotated[AsyncSession, Depends(get_session)]
ServiceDep = Annotated[ComplaintService, FromDishka()]


@router.post("/complaints")
async def create_complaint(
    complaint_data: ComplaintCreate, db: SessionDep, complaint_service: ServiceDep
):
    try:
        complaint = await complaint_service.create_complaint(
            db,
            description=complaint_data.description,
            district=complaint_data.district,
            status=complaint_data.status,
            executor_id=complaint_data.executor_id,
            address=complaint_data.address,
        )
        return ComplaintDTO(
            complaint_id=complaint.complaint_id,
            status=complaint.status,
            executor_id=complaint.executor_id,
            address=complaint.address,
            district=complaint.district,
            description=complaint.description,
            resolution=complaint.resolution,
            created_at=complaint.created_at,
            execution_date=complaint.execution_date,
            final_status_at=complaint.final_status_at,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/complaints/{complaint_id}")
async def get_complaint(
    complaint_id: int, db: SessionDep, complaint_service: ServiceDep
):
    complaint = await complaint_service.get_complaint(db, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return ComplaintDTO(
        complaint_id=complaint.complaint_id,
        status=complaint.status,
        executor_id=complaint.executor_id,
        address=complaint.address,
        district=complaint.district,
        description=complaint.description,
        resolution=complaint.resolution,
        created_at=complaint.created_at,
        execution_date=complaint.execution_date,
        final_status_at=complaint.final_status_at,
    )


@router.put("/complaints/{complaint_id}")
async def update_complaint(
    complaint_id: int,
    complaint_data: ComplaintUpdate,
    db: SessionDep,
    complaint_service: ServiceDep,
):
    complaint = await complaint_service.update_complaint(
        db,
        complaint_id=complaint_id,
        status=complaint_data.status,
        resolution=complaint_data.resolution,
        executor_id=complaint_data.executor_id,
        address=complaint_data.address,
    )
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return ComplaintDTO(
        complaint_id=complaint.complaint_id,
        status=complaint.status,
        executor_id=complaint.executor_id,
        address=complaint.address,
        district=complaint.district,
        description=complaint.description,
        resolution=complaint.resolution,
        created_at=complaint.created_at,
        execution_date=complaint.execution_date,
        final_status_at=complaint.final_status_at,
    )


@router.delete("/complaints/{complaint_id}")
async def delete_complaint(
    complaint_id: int, db: SessionDep, complaint_service: ServiceDep
):
    try:
        await complaint_service.delete_complaint(db, complaint_id)
        return {"detail": "Complaint deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================================
# Ручки для работы с исполнителями (Executor)
# ================================


@router.post("/executors")
async def create_executor(
    executor_data: ExecutorUpdateRequest, db: SessionDep, complaint_service: ServiceDep
):
    executor = await complaint_service.create_executor(
        db,
        name=executor_data.name,
        organization=executor_data.organization,
        phone=executor_data.phone,
        email=executor_data.email,
    )
    return ExecutorDTO(
        executor_id=executor.executor_id,
        name=executor.name,
        organization=executor.organization,
        phone=executor.phone,
        email=executor.email,
        is_active=executor.is_active,
    )


@router.get("/executors/{executor_id}")
async def get_executor(executor_id: int, db: SessionDep, complaint_service: ServiceDep):
    executor = await complaint_service.get_executor(db, executor_id)
    if not executor:
        raise HTTPException(status_code=404, detail="Executor not found")
    return ExecutorDTO(
        executor_id=executor.executor_id,
        name=executor.name,
        organization=executor.organization,
        phone=executor.phone,
        email=executor.email,
        is_active=executor.is_active,
    )


@router.put("/executors/{executor_id}")
async def update_executor(
    executor_id: int,
    executor_data: ExecutorUpdateRequest,
    db: SessionDep,
    complaint_service: ServiceDep,
):
    executor = await complaint_service.update_executor(
        db,
        executor_id=executor_id,
        name=executor_data.name,
        organization=executor_data.organization,
        phone=executor_data.phone,
        email=executor_data.email,
    )
    if not executor:
        raise HTTPException(status_code=404, detail="Executor not found")
    return ExecutorDTO(
        executor_id=executor.executor_id,
        name=executor.name,
        organization=executor.organization,
        phone=executor.phone,
        email=executor.email,
        is_active=executor.is_active,
    )


@router.delete("/executors/{executor_id}")
async def delete_executor(
    executor_id: int, db: SessionDep, complaint_service: ServiceDep
):
    try:
        await complaint_service.delete_executor(db, executor_id)
        return {"detail": "Executor deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================================
# Ручка для обновления статуса исполнителя по заявке
# ================================


@router.put("/complaints/{complaint_id}/executor-update")
async def handle_executor_update(
    complaint_id: int,
    executor_update: ExecutorUpdateRequest,
    db: SessionDep,
    complaint_service: ServiceDep,
):
    try:
        complaint = await complaint_service.handle_executor_update(
            db, complaint_id=complaint_id, update=executor_update
        )
        return ComplaintDTO(
            complaint_id=complaint.complaint_id,
            status=complaint.status,
            executor_id=complaint.executor_id,
            address=complaint.address,
            district=complaint.district,
            description=complaint.description,
            resolution=complaint.resolution,
            created_at=complaint.created_at,
            execution_date=complaint.execution_date,
            final_status_at=complaint.final_status_at,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/moderators")
async def create_moderator(
    moderator_data: ModeratorCreate, db: SessionDep, complaint_service: ServiceDep
):
    try:
        moderator = await complaint_service.create_moderator(
            db,
            username=moderator_data.username,
            full_name=moderator_data.full_name,
            email=moderator_data.email,
            phone=moderator_data.phone,
        )
        return ModeratorDTO(
            moderator_id=moderator.moderator_id,
            username=moderator.username,
            full_name=moderator.full_name,
            email=moderator.email,
            phone=moderator.phone,
            is_active=moderator.is_active,
            complaint_id=moderator.complaint_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/moderators/{moderator_id}")
async def get_moderator(
    moderator_id: int, db: SessionDep, complaint_service: ServiceDep
):
    moderator = await complaint_service.get_moderator(db, moderator_id)
    if not moderator:
        raise HTTPException(status_code=404, detail="Moderator not found")
    return ModeratorDTO(
        moderator_id=moderator.moderator_id,
        username=moderator.username,
        full_name=moderator.full_name,
        email=moderator.email,
        phone=moderator.phone,
        is_active=moderator.is_active,
        complaint_id=moderator.complaint_id,
    )


@router.put("/moderators/{moderator_id}")
async def update_moderator(
    moderator_id: int,
    moderator_data: ModeratorUpdate,
    db: SessionDep,
    complaint_service: ServiceDep,
):
    moderator = await complaint_service.update_moderator(
        db,
        moderator_id=moderator_id,
        username=moderator_data.username,
        full_name=moderator_data.full_name,
        email=moderator_data.email,
        phone=moderator_data.phone,
    )
    if not moderator:
        raise HTTPException(status_code=404, detail="Moderator not found")
    return ModeratorDTO(
        moderator_id=moderator.moderator_id,
        username=moderator.username,
        full_name=moderator.full_name,
        email=moderator.email,
        phone=moderator.phone,
        is_active=moderator.is_active,
        complaint_id=moderator.complaint_id,
    )


@router.delete("/moderators/{moderator_id}")
async def delete_moderator(
    moderator_id: int, db: SessionDep, complaint_service: ServiceDep
):
    try:
        await complaint_service.delete_moderator(db, moderator_id)
        return {"detail": "Moderator deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
