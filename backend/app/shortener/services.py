from urllib.parse import urljoin

from app.settings.config import settings
from app.shortener.models import Url
from app.shortener.repository import ShortenerRepository
from app.shortener.schemas import SUrlBase, SUrlInfo, SAddUrl, STargetUrl
from app.shortener.utils import create_unique_random_key


async def create_url(url: SUrlBase) -> SAddUrl:
    """
     Create a new URL in the database.

     Args:
         url (SUrlBase): The URL to create.

     """
    key_ = await create_unique_random_key()

    result = await ShortenerRepository.add_url(
        data=dict(target_url=url.target_url, key=key_),
    )

    base_url = f'{settings().DOMAIN}:{settings().DOMAIN_PORT}'  # todo: generate base url in conf or env
    result.url = urljoin(base_url, result.key)

    return result


async def get_active_long_url_by_key(key: str) -> SUrlInfo | None:
    """
    Get a URL from the database by its key.

    Args:
        key (str): The key of the URL to get.

    """
    if long_url := await ShortenerRepository.get_active_long_url(url_key=key):
        return long_url

    return None


async def update_db_clicks(url: SUrlInfo) -> STargetUrl:
    """
    Update the clicks count for a URL in the database.

    Args:
        url (SUrlInfo): The URL to update.

    Returns:
        Url: The updated URL.
    """
    return await ShortenerRepository.update_redirect_counter(url)
