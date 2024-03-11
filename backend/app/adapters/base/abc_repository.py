from abc import ABC, abstractmethod
from typing import Any


class ABCRepository(ABC):
    @abstractmethod
    async def add(self, *, data: dict) -> int:
        ...

    @abstractmethod
    async def update(self, model_id: int, **update_data: Any):
        ...
