from sqlalchemy import update

from app.core.repository import SQLAlchemyRepository
from app.shortener.models import Url
from app.shortener.schemas import SUrlInfo


class ShortenerRepository(SQLAlchemyRepository):
    model = Url

    async def add_url(self, *, data: dict):
        return await super().add_entity(data=data)

    async def get_url_by_id(self, *, id_: int):
        return await super().find_by_id(model_id=id_)

    async def get_active_long_url(self, *, url_key: str):
        return await super().find_one_or_none(key=url_key, is_active=True)

    async def update_redirect_counter(self, *, url_: SUrlInfo):
        statement = (
            update(self.model)
            .filter_by(id=url_.id)
            .values(clicks_count=url_.clicks_count + 1)
        )
        await self.session.execute(statement)
