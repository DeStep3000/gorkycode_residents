from datetime import datetime

from pydantic import BaseModel


class ExecutorDTO(BaseModel):
    executor_id: int
    name: int
    organization: int | None
    phone: str | None
    email: str | None
    is_active: bool


class ComplaintDTO(BaseModel):
    complaint_id: int

    # В БД TIMESTAMP WITHOUT TIME ZONE → timezone=False (по умолчанию)
    created_at: datetime | None
    execution_date: datetime | None
    final_status_at: datetime | None
    status: str
    address: str

    executor_id: int | None

    district: str | None
    description: str
    resolution: str | None


class ModeratorDTO(BaseModel):

    moderator_id: int

    username: str
    full_name: str
    email: str | None
    phone: str | None
    is_active: bool

    complaint_id: int | None