from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    Text,
    DateTime,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
import enum


class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"


class Sender(Base):  # пользователь
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))
    fathername: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum), default=RoleEnum.user, nullable=False
    )

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="sender")


class Service(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)

    categories: Mapped[list["Category"]] = relationship(back_populates="service")


class Category(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))

    service: Mapped[Service] = relationship(back_populates="categories")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="category")


class Ticket(Base):  # заявка
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    relevance: Mapped[int] = mapped_column(Integer, default=5)

    sender_id: Mapped[int] = mapped_column(ForeignKey("sender.id"))
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("category.id"), nullable=True
    )

    sender: Mapped[Sender] = relationship(back_populates="tickets")
    category: Mapped[Category | None] = relationship(back_populates="tickets")
    messages: Mapped[list["Message"]] = relationship(back_populates="ticket")


class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"


class Message(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("ticket.id"))
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ticket: Mapped[Ticket] = relationship(back_populates="messages")
