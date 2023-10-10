from urllib.parse import urljoin

from app.core.unit_of_work import ABCUnitOfWork
from app.settings.config import settings
from app.shortener.schemas import SAddUrl, SUrlInfo
from app.shortener.utils import create_unique_random_key


class ShortenerServices:
    async def get_active_long_url_by_key(
        self,
        *,
        key: str,
        uow: ABCUnitOfWork,
    ) -> SUrlInfo | None:
        """
        Get a URL from the database by its key.

        Args:
            key (str): The key of the URL to get.
            uow (ABCUnitOfWork): ...
        """
        async with uow:
            if long_url := await uow.shortener_repo.get_active_long_url(url_key=key):
                await uow.commit()
                return long_url

            return None

    async def create_url(self, *, target_url: str, uow: ABCUnitOfWork) -> SAddUrl:
        """
        Create a new URL in the database.

        Args:
            target_url (str): The URL to create.
            uow (ABCUnitOfWork): ...
        """
        key_ = await create_unique_random_key(uow=uow)

        async with uow:
            result = await uow.shortener_repo.add_url(
                data={
                    'target_url': target_url,
                    'key': key_,
                },
            )
            result.url = urljoin(settings().BASE_URL, result.key)
            await uow.commit()

            return result

    async def update_db_clicks(self, *, url: SUrlInfo, uow: ABCUnitOfWork):
        """
        Update the clicks count for a URL in the database.

        Args:
            url (SUrlInfo): The URL to update.
            uow (ABCUnitOfWork): ...
        """
        async with uow:
            await uow.shortener_repo.update_redirect_counter(url_=url)
            await uow.commit()
