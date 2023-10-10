from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

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
        return self

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...


class UnitOfWork(ABCUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

        self._session = None
        self._shortener_repo = None

    @property
    def session(self) -> AsyncSession:
        if not self._session:
            self._session = self.session_factory()
        return self._session

    @property
    def shortener_repo(self) -> ShortenerRepository:
        if not self._shortener_repo:
            self._shortener_repo = ShortenerRepository(session=self.session)
        return self._shortener_repo

    async def __aenter__(self) -> ABCUnitOfWork:
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
