from abc import ABC, abstractmethod
from typing import Type, TypeVar

from sqlalchemy import select, insert

from app.settings.database import Base, async_session_maker

ModelType = TypeVar('ModelType', bound=Base)


class ABCRepository(ABC):

    @classmethod
    @abstractmethod
    async def add_entity(cls, data: dict) -> int: ...

    @classmethod
    @abstractmethod
    async def find_by_id(cls, model_id: int): ...

    @classmethod
    @abstractmethod
    async def find_one_or_none(cls): ...


class SQLAlchemyRepository(ABCRepository):
    model: Type[ModelType] = None

    @classmethod
    async def add_entity(cls, data: dict) -> int:
        async with async_session_maker() as session:
            statement = insert(cls.model).values(**data).returning(cls.model.id)

            statement_result = await session.execute(statement=statement)
            await session.commit()

            return statement_result.scalar_one()

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            query_result = await session.execute(query)

            return query_result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            query_result = await session.execute(query)

            return query_result.scalar_one_or_none()
