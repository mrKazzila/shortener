from app.core.repository import SQLAlchemyRepository
from app.shortener.models import Url


class ShortenerRepository(SQLAlchemyRepository):
    model = Url

    @classmethod
    async def add_url(cls, data: dict) -> int:
        result = await super().add_entity(data=data)
        return result

    @classmethod
    async def get_url_by_id(cls, id_: int):
        url_ = await super().find_by_id(model_id=id_)
        return url_
