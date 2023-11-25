from typing import Any, Type, TypeVar

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.abc_repository import ABCRepository
from app.settings.database import Base

ModelType = TypeVar('ModelType', bound=Base)


class SQLAlchemyRepository(ABCRepository):
    __slots__ = ('session',)
    model: Type[ModelType] = None

    def __init__(self, *, session: AsyncSession) -> None:
        self.session = session

    async def add(self, *, data: dict):
        """Add new entity."""
        statement = insert(self.model).values(**data).returning(self.model)
        statement_result = await self.session.execute(statement=statement)

        return statement_result.scalar_one()

    async def find(self, *, model_id: int):
        """Find entity by model id."""
        query = select(self.model).filter_by(id=model_id)
        query_result = await self.session.execute(query)

        return query_result.scalar_one_or_none()

    async def search(self, **reference: Any):
        """Search entity by some reference."""
        query = select(self.model).filter_by(**reference)
        query_result = await self.session.execute(query)

        return query_result.scalar_one_or_none()

    async def update(self, *, model_id: int, **update_data: Any):
        """Update entity some data."""
        statement = update(self.model).filter_by(id=model_id).values(**update_data)
        await self.session.execute(statement)
