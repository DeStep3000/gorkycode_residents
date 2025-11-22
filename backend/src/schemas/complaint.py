# app/schemas/complaint.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import StrEnum


class ComplaintStatus(StrEnum):
    NEW = "new"
    ASSIGNED_RESPONSIBLE = "assigned_responsible"
    IN_PROGRESS_RESPONSIBLE = "in_progress_responsible"
    MODERATED = "moderated"
    CLOSED = "closed"
    BLOCK_WORKFLOW = "block_workflow"


class ComplaintCreate(BaseModel):
    description: str
    district: str | None = None
    status: ComplaintStatus
    executor_id: str | None = None
    address: str


# Для обновления существующей жалобы
class ComplaintUpdate(BaseModel):
    status: Optional[ComplaintStatus] = None
    resolution: Optional[str] = None
    executor_id: Optional[int] = None
    address: Optional[str] = None


# Для чтения жалобы (детали)
class ComplaintRead(BaseModel):
    complaint_id: int
    description: str
    district: Optional[str]
    status: ComplaintStatus
    executor_id: Optional[int]
    address: str
    resolution: Optional[str]
    created_at: datetime
    execution_date: Optional[datetime]
    final_status_at: Optional[datetime]


# Для списка жалоб (сокращенная информация)
class ComplaintList(BaseModel):
    complaint_id: int
    description: str
    status: ComplaintStatus
    executor_id: Optional[int]
    address: str
    created_at: datetime


# ============================
# Moderator Pydantic Schemas
# ============================


# Для создания нового модератора
class ModeratorCreate(BaseModel):
    username: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None


# Для обновления данных модератора
class ModeratorUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


# Для чтения информации о модераторе
class ModeratorRead(BaseModel):
    moderator_id: int
    username: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
