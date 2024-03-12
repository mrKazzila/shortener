from abc import ABC, abstractmethod
from typing import Any

__all__ = ['ABCRepository']


class ABCRepository(ABC):
    @abstractmethod
    async def add(self, *, data: dict) -> int:
        ...

    @abstractmethod
    async def update(self, model_id: int, **update_data: Any):
        ...
