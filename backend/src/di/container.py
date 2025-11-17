from collections.abc import AsyncIterator

from dishka import (
    provide,
    Scope,
    Provider,
    make_async_container,
)
from dishka.integrations.fastapi import FastapiProvider
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.ai_protocol import AIClient
from src.adapters.repo_protocols import SenderRepo, TicketRepo, MessageRepo
from src.db.session import SessionFactory
from src.adapters.repo_sqlalchemy import (
    SenderRepoImpl,
    TicketRepoImpl,
    MessageRepoImpl,
)
from src.adapters.ai_openai import EchoAIClient
from src.services.auth import AuthService
from src.services.tickets import TicketService
from src.services.chat import ChatService


class AppProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with SessionFactory() as session:
            async with session.begin():
                yield session

    sender_repo = provide(source=SenderRepoImpl, provides=SenderRepo)
    ticket_repo = provide(source=TicketRepoImpl, provides=TicketRepo)
    message_repo = provide(source=MessageRepoImpl, provides=MessageRepo)

    ai_client = provide(source=EchoAIClient, provides=AIClient)

    auth_service = provide(AuthService)
    ticket_service = provide(TicketService)
    chat_service = provide(ChatService)


provider = AppProvider()
container = make_async_container(provider, FastapiProvider())
