from app.core.repository import SQLAlchemyRepository
from app.shortener.models import Url
from app.shortener.schemas import SUrl
from sqlalchemy import update
from app.settings.database import async_session_maker


class ShortenerRepository(SQLAlchemyRepository):
    model = Url

    @classmethod
    async def add_url(cls, data: dict):
        result = await super().add_entity(data=data)
        return result

    @classmethod
    async def get_url_by_id(cls, id_: int):
        url_ = await super().find_by_id(model_id=id_)
        return url_

    @classmethod
    async def get_active_long_url(cls, url_key: str):
        query_result = await super().find_one_or_none(key=url_key, is_active=True)
        return query_result

    @classmethod
    async def update_redirect_counter(cls, url_):
        async with async_session_maker() as session:
            statement = (
                update(cls.model)
                .filter_by(id=url_.id)
                .values(clicks_count=url_.clicks_count+1)
            )

            await session.execute(statement)
            await session.commit()

            return url_
