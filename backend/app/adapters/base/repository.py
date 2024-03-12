from typing import Any, TypeVar

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.base import ABCRepository
from app.settings.database import Base

ModelType = TypeVar("ModelType", bound=Base)

__all__ = ["SQLAlchemyRepository"]


class SQLAlchemyRepository(ABCRepository):
    __slots__ = ("session",)
    model: type[ModelType] = None

    def __init__(self, *, session: AsyncSession) -> None:
        self.session = session

    def __repr__(self) -> str:
        return "Main repository for SQLAlchemy"

    async def add(self, *, data: dict) -> type[ModelType]:
        """Add new entity."""
        _statement = insert(self.model).values(**data).returning(self.model)
        statement_result = await self.session.execute(statement=_statement)

        return statement_result.scalar_one()

    async def get(self, *, reference: dict) -> type[ModelType] | None:
        """Get entity by some reference."""
        _statement = select(self.model).filter_by(**reference)
        statement_result = await self.session.execute(statement=_statement)

        return statement_result.scalar_one_or_none()

    async def update(self, *, model_id: int, **update_data: Any):
        """Update entity some data."""
        _statement = (
            update(self.model)
            .filter_by(id=model_id)
            .values(**update_data)
        )
        await self.session.execute(_statement)
