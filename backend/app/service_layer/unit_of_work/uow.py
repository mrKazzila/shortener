from sqlalchemy.ext.asyncio import AsyncSession

from app.api.urls.repository import ShortenerRepository
from service_layer.unit_of_work.abc_uow import ABCUnitOfWork
from app.settings.database import async_session_maker


class UnitOfWork(ABCUnitOfWork):
    __slots__ = ('session_factory',)

    def __init__(self, session_factory=async_session_maker) -> None:
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
