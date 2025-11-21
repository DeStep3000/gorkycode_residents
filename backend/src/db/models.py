from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
    ARRAY,
    text,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.base import Base
from enum import StrEnum


class ComplaintStatus(StrEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    REDIRECTED = "redirected"


class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    status: Mapped[str] = mapped_column(
        String, default=ComplaintStatus.NEW.value, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    description: Mapped[str] = mapped_column(String, nullable=False)
    district: Mapped[str] = mapped_column(String, nullable=True)
    resolution: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    execution_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    executor_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    final_status_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    history: Mapped["ComplaintHistory"] = relationship(
        "ComplaintHistory",
        back_populates="complaint",
        uselist=False,
        cascade="all, delete-orphan",
    )


class ComplaintHistory(Base):
    """
    Одна запись на complaint_id:
    - executors_ids: список id исполнителей, которые уже трогали заявку (в порядке).
    - responses: JSON вида {executor_id: {"response": "...", "timestamp": "..."}}
    """

    __tablename__ = "complaint_histories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    complaint_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaints.complaint_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    executors_ids: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    responses: Mapped[dict] = mapped_column(JSON, default=dict)

    complaint: Mapped[Complaint] = relationship("Complaint", back_populates="history")
