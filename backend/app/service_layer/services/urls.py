import logging

from app.api.urls import utils
from app.schemas.urls import SUrl, SUrlInfo
from app.service_layer.unit_of_work import UnitOfWork

__all__ = ("UrlsServices",)

logger = logging.getLogger(__name__)


class UrlsServices:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    @staticmethod
    async def get_active_long_url_by_key(
        *,
        key: str,
        uow: UnitOfWork,
    ) -> SUrlInfo | None:
        """Get a URL from the database by its key."""
        _reference = {"key": key}

        async with uow:
            if long_url := await uow.urls_repo.get(reference=_reference):
                return SUrlInfo.model_validate(long_url)
        return None

    @classmethod
    async def create_url(
        cls,
        *,
        target_url: str,
        uow: UnitOfWork,
    ) -> SUrl:
        """Create a new URL in the database."""
        key_ = await cls._create_unique_random_key(uow=uow)

        async with uow:
            result = await uow.urls_repo.add(target_url=target_url, key=key_)
            await uow.commit()

        return SUrl.model_validate(result)

    @staticmethod
    async def update_db_clicks(
        *,
        url: SUrlInfo,
        uow: UnitOfWork,
    ) -> None:
        """Update the clicks count for a URL in the database."""
        incremented_clicks_count = url.clicks_count + 1

        async with uow:
            await uow.urls_repo.update(
                model_id=url.id,
                clicks_count=incremented_clicks_count,
            )
            await uow.commit()

    @classmethod
    async def _create_unique_random_key(cls, *, uow: UnitOfWork) -> str:
        """Creates a unique random key."""
        key = utils.generate_random_key()

        while await cls.get_active_long_url_by_key(
            key=key,
            uow=uow,
        ):
            key = utils.generate_random_key()

        return key
