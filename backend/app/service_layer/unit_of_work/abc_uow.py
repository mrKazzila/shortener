from abc import ABC, abstractmethod

__all__ = ("ABCUnitOfWork",)


class ABCUnitOfWork(ABC):
    async def __aenter__(self) -> None:
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...
