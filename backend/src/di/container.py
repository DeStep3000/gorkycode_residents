from dishka import (
    provide,
    Scope,
    Provider,
    make_async_container,
)
from dishka.integrations.fastapi import FastapiProvider

from src.adapters.notifier import DummyNotifier
from src.protocols.ai import AIClientProtocol
from src.protocols.notifier import NotifierProtocol
from src.protocols.repo import (
    ComplaintRepositoryProtocol,
    ExecutorRepositoryProtocol,
    ModeratorRepositoryProtocol,
    TicketStatusRepositoryProtocol,
)
from src.adapters.repo import (
    ComplaintRepository,
    ModeratorRepository,
    TicketStatusRepository,
    ExecutorRepository,
)
from src.adapters.ai import YandexAIClient

from src.services.complaints import ComplaintService


class AppProvider(Provider):
    scope = Scope.APP

    complaints_repo = provide(
        source=ComplaintRepository, provides=ComplaintRepositoryProtocol
    )
    executor_repo = provide(
        source=ExecutorRepository, provides=ExecutorRepositoryProtocol
    )
    moderator_repo = provide(
        source=ModeratorRepository, provides=ModeratorRepositoryProtocol
    )
    ticket_repo = provide(
        source=TicketStatusRepository, provides=TicketStatusRepositoryProtocol
    )
    ai_adapter = provide(source=YandexAIClient, provides=AIClientProtocol)
    notifier_adapter = provide(source=DummyNotifier, provides=NotifierProtocol)

    complaints_service = provide(ComplaintService)


provider = AppProvider()
container = make_async_container(provider, FastapiProvider())
