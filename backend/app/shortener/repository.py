from sqlalchemy import update

from app.core.repository import SQLAlchemyRepository
from app.settings.database import async_session_maker
from app.shortener.models import Url
from app.shortener.schemas import SUrlInfo


class ShortenerRepository(SQLAlchemyRepository):
    model = Url

    @classmethod
    async def add_url(cls, data: dict):
        return await super().add_entity(data=data)

    @classmethod
    async def get_url_by_id(cls, id_: int):
        return await super().find_by_id(model_id=id_)

    @classmethod
    async def get_active_long_url(cls, url_key: str):
        return await super().find_one_or_none(key=url_key, is_active=True)

    @classmethod
    async def update_redirect_counter(cls, url_: SUrlInfo):
        async with async_session_maker() as session:
            statement = (
                update(cls.model)
                .filter_by(id=url_.id)
                .values(clicks_count=url_.clicks_count + 1)
            )

            await session.execute(statement)
            await session.commit()

            return url_
