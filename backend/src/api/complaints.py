# app/api/v1/complaints.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from dishka.integrations.fastapi import inject, FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_session
from src.schemas.complaint import (
    ComplaintCreate,
    ComplaintRead,
    ComplaintList,
    ComplaintUpdate,
    ComplaintHistoryRead,
)
from src.schemas.executor_update import ExecutorUpdateRequest
from src.services.complaints import ComplaintService

router = APIRouter(prefix="/complaints", tags=["complaints"])


SessionDep = Annotated[AsyncSession, Depends(get_session)]
ServiceDep = Annotated[ComplaintService, FromDishka()]


@router.post("/", response_model=ComplaintRead)
@inject
async def create_complaint(
    data: ComplaintCreate,
    session: SessionDep,
    service: ServiceDep,
):
    complaint = await service.create_complaint(session, data)
    return complaint


@router.get("/{complaint_id}", response_model=ComplaintRead)
@inject
async def get_complaint(
    complaint_id: int,
    session: SessionDep,
    service: ServiceDep,
):
    complaint = await service.get_complaint(session, complaint_id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


@router.get("/", response_model=ComplaintList)
@inject
async def list_complaints(
    session: SessionDep,
    service: ServiceDep,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    items, total = await service.list_complaints(session, limit=limit, offset=offset)
    return ComplaintList(items=items, total=total)


@router.patch("/{complaint_id}", response_model=ComplaintRead)
@inject
async def update_complaint(
    complaint_id: int,
    data: ComplaintUpdate,
    session: SessionDep,
    service: ServiceDep,
):
    complaint = await service.update_complaint(session, complaint_id, data)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


@router.get("/{complaint_id}/history", response_model=ComplaintHistoryRead)
@inject
async def get_complaint_history(
    complaint_id: int,
    session: SessionDep,
    service: ServiceDep,
):
    history = await service.get_history(session, complaint_id)
    return ComplaintHistoryRead(
        complaint_id=history.complaint_id,
        executors_ids=history.executors_ids,
        responses=history.responses,
    )


@router.post("/{complaint_id}/executor-update", response_model=ComplaintRead)
@inject
async def executor_update(
    complaint_id: int,
    update: ExecutorUpdateRequest,
    session: SessionDep,
    service: ServiceDep,
):
    complaint = await service.handle_executor_update(session, complaint_id, update)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint
