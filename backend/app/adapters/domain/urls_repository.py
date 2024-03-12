from app.adapters.base import SQLAlchemyRepository
from app.models import Urls

__all__ = ['UrlsRepository']


class UrlsRepository(SQLAlchemyRepository):
    model = Urls

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} for model: {self.model}"
