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
    ComplaintHistoryRepositoryProtocol,
)
from src.adapters.repo import (
    ComplaintRepository,
    ComplaintHistoryRepository,
)
from src.adapters.ai import DummyAIClient

from src.services.complaints import ComplaintService


class AppProvider(Provider):
    scope = Scope.APP

    complaints_repo = provide(
        source=ComplaintRepository, provides=ComplaintRepositoryProtocol
    )
    complaints_history_repo = provide(
        source=ComplaintHistoryRepository, provides=ComplaintHistoryRepositoryProtocol
    )
    ai_adapter = provide(source=DummyAIClient, provides=AIClientProtocol)
    notifier_adapter = provide(source=DummyNotifier, provides=NotifierProtocol)

    complaints_service = provide(ComplaintService)


provider = AppProvider()
container = make_async_container(provider, FastapiProvider())
