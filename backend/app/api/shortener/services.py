from urllib.parse import urljoin

from app.api.shortener import schemas, utils
from app.service_layer.unit_of_work import UnitOfWork
from app.settings.config import settings


class ShortenerServices:
    async def get_active_long_url_by_key(
            self,
            *,
            key: str,
            uow: UnitOfWork,
    ) -> schemas.SUrlInfo | None:
        """
        Get a URL from the database by its key.

        Args:
            key (str): The key of the URL to get.
            uow (UnitOfWork): ...
        """
        async with uow:
            if long_url := await uow.shortener_repo.search(url_key=key):
                await uow.commit()
                return long_url

            return None

    async def create_url(
            self,
            *,
            target_url: str,
            uow: UnitOfWork,
    ) -> schemas.SUrl:
        """
        Create a new URL in the database.

        Args:
            target_url (str): The URL to create.
            uow (UnitOfWork): ...
        """
        key_ = await self._create_unique_random_key(uow=uow)

        async with uow:
            result = await uow.shortener_repo.add(
                data={
                    'target_url': target_url,
                    'key': key_,
                },
            )
            result.url = urljoin(base=settings().BASE_URL, url=result.key)
            await uow.commit()

            return result

    async def update_db_clicks(
            self,
            *,
            url: schemas.SUrlInfo,
            uow: UnitOfWork,
    ) -> None:
        """
        Update the clicks count for a URL in the database.

        Args:
            url (SUrlInfo): The URL to update.
            uow (UnitOfWork): ...
        """
        incremented_clicks_count = url.clicks_count + 1

        async with uow:
            await uow.shortener_repo.update(
                model_id=url.id,
                clicks_count=incremented_clicks_count,
            )
            await uow.commit()

    async def _create_unique_random_key(self, *, uow: UnitOfWork) -> str:
        """
        Creates a unique random key.

        Returns:
            A unique random key.
        """
        key = utils.generate_random_key()

        while await self.get_active_long_url_by_key(
                key=key,
                uow=uow,
        ):
            key = utils.generate_random_key()

        return key
