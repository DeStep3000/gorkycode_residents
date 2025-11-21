# app/schemas/complaint.py
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field

from src.db.models import ComplaintStatus


class ComplaintBase(BaseModel):
    description: str
    district: Optional[str] = None


class ComplaintCreate(ComplaintBase):
    # Житель создаёт заявку
    executor_id: Optional[str] = (
        None  # можно сразу проставлять исполнителя (если есть логика маршрутизации)
    )


class ComplaintUpdate(BaseModel):
    # Обновление модератором
    status: Optional[ComplaintStatus] = None
    resolution: Optional[str] = None
    executor_id: Optional[str] = None
    execution_date: Optional[datetime] = None
    final_status_at: Optional[datetime] = None


class ComplaintRead(BaseModel):
    complaint_id: int
    status: ComplaintStatus
    created_at: datetime
    description: str
    district: Optional[str]
    resolution: Optional[str]
    execution_date: Optional[datetime]
    executor_id: Optional[str]
    final_status_at: Optional[datetime]

    class Config:
        from_attributes = True


class ComplaintList(BaseModel):
    items: list[ComplaintRead]
    total: int


class ComplaintHistoryRead(BaseModel):
    complaint_id: int
    executors_ids: List[str] = Field(default_factory=list)
    responses: Dict[str, dict] = Field(default_factory=dict)
