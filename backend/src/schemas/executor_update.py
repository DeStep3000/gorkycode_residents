from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExecutorUpdateRequest(BaseModel):
    executor_id: str
    response_text: str
    status: Optional[str] = None  # например, "done", "in_progress" и т.д.
    executed_at: Optional[datetime] = None


class ExecutorUpdateResult(BaseModel):
    decision: str
    is_forward: bool
    is_blocking_bounce: bool
    target_executor_name: Optional[str] = None
    moderator_message: Optional[str] = None
    ai_badge: Optional[str] = None
