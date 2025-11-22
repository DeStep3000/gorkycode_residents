# db/models.py

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


# ============================
# EXECUTORS
# ============================


class Executor(Base):
    __tablename__ = "executors"

    executor_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    organization: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # заявки, где этот исполнитель текущий
    complaints: Mapped[List["Complaint"]] = relationship(
        back_populates="executor",
        foreign_keys="Complaint.executor_id",
    )


# ============================
# COMPLAINTS
# ============================


class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )

    # В БД TIMESTAMP WITHOUT TIME ZONE → timezone=False (по умолчанию)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,  # возвращает naive datetime
        nullable=False,
    )
    execution_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    final_status_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(String(50), nullable=False)

    executor_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("executors.executor_id"),
        nullable=True,
    )

    district: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- relationships ---

    executor: Mapped[Optional["Executor"]] = relationship(
        back_populates="complaints",
        foreign_keys=[executor_id],
    )

    # одна заявка → много модераторов (в таблице moderators FK complaint_id)
    moderators: Mapped[List["Moderator"]] = relationship(
        back_populates="complaint",
    )

    ticket_statuses: Mapped[List["TicketStatus"]] = relationship(
        back_populates="complaint",
        cascade="all, delete-orphan",
    )


# ============================
# MODERATORS
# ============================


class Moderator(Base):
    __tablename__ = "moderators"

    moderator_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )

    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    complaint_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("complaints.complaint_id"),
        nullable=True,
    )

    # --- relationships ---

    complaint: Mapped[Optional["Complaint"]] = relationship(
        back_populates="moderators",
    )


# ============================
# TICKETSTATUSES
# ============================


class TicketStatus(Base):
    __tablename__ = "ticket_statuses"

    # составной первичный ключ: status_code + complaint_id + data
    status_code: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )
    complaint_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("complaints.complaint_id", ondelete="CASCADE"),
        primary_key=True,
    )
    data: Mapped[datetime] = mapped_column(
        DateTime,
        primary_key=True,
        default=datetime.utcnow,  # naive datetime
    )

    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- relationships ---

    complaint: Mapped["Complaint"] = relationship(
        back_populates="ticket_statuses",
    )
