from abc import ABC, abstractmethod
from typing import Any


class ABCRepository(ABC):
    @abstractmethod
    async def add(self, *, data: dict) -> int:
        ...

    @abstractmethod
    async def find(self, *, model_id: int):
        ...

    @abstractmethod
    async def search(self, **filter_by: Any):
        ...

    @abstractmethod
    async def update(self, model_id: int, **update_data: Any):
        ...
