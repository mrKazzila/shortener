from app.adapters.base import SQLAlchemyRepository
from app.models import Urls

__all__ = ("UrlsRepository",)


class UrlsRepository(SQLAlchemyRepository):
    """Urls repository."""

    model = Urls
