from abc import ABC, abstractmethod

__all__ = ("ABCRepository",)


class ABCRepository(ABC):
    @abstractmethod
    async def add(self, *, data):
        ...

    @abstractmethod
    async def update(self, model_id, **update_data):
        ...
