from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExecutorUpdateRequest(BaseModel):
    executor_id: int
    response_text: str
    status: Optional[str] = None  # например, "done", "in_progress" и т.д.
    executed_at: Optional[datetime] = None


class ExecutorUpdateResult(BaseModel):
    is_forward: bool
    target_executor_name: Optional[str] = None
    is_blocking_bounce: bool = False
    notes: Optional[str] = None
