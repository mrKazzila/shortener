from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings.database import Base

ModelType = TypeVar('ModelType', bound=Base)


class ABCRepository(ABC):
    @abstractmethod
    async def add_entity(self, *, data: dict) -> int:
        ...

    @abstractmethod
    async def find_by_id(self, *, model_id: int):
        ...

    @abstractmethod
    async def find_one_or_none(self, **filter_by: Any):
        ...


class SQLAlchemyRepository(ABCRepository):
    model: Type[ModelType] = None

    def __init__(self, *, session: AsyncSession):
        self.session = session

    async def add_entity(self, *, data: dict):
        statement = insert(self.model).values(**data).returning(self.model)
        statement_result = await self.session.execute(statement=statement)

        return statement_result.scalar_one()

    async def find_by_id(self, *, model_id: int):
        query = select(self.model).filter_by(id=model_id)
        query_result = await self.session.execute(query)

        return query_result.scalar_one_or_none()

    async def find_one_or_none(self, **filter_by: Any):
        query = select(self.model).filter_by(**filter_by)
        query_result = await self.session.execute(query)

        return query_result.scalar_one_or_none()
