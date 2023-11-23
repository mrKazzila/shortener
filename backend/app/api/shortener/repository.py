from typing import Any

from app.adapters.repository import SQLAlchemyRepository
from app.api.shortener.models import Url


class ShortenerRepository(SQLAlchemyRepository):
    model = Url

    async def add(self, *, data: dict):
        return await super().add(data=data)

    async def find(self, *, id_: int):
        return await super().find(model_id=id_)

    async def search(self, *, url_key: str):
        return await super().search(key=url_key, is_active=True)

    async def update(self, *, model_id: int, **update_data: Any):
        return await super().update(model_id=model_id, **update_data)
