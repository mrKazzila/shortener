from abc import ABC, abstractmethod

from app.settings.database import async_session_maker
from app.shortener.repository import ShortenerRepository

DEFAULT_SESSION_FACTORY = async_session_maker


class ABCUnitOfWork(ABC):
    shortener_repo: ShortenerRepository

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(ABCUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.shortener_repo = ShortenerRepository(session=self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
