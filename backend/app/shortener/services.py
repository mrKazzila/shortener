from app.settings.config import settings
from app.shortener.keygen import create_unique_random_key
from app.shortener.models import Url
from app.shortener.repository import ShortenerRepository
from app.shortener.schemas import SUrlBase, SUrlInfo, SAddUrl
from app.shortener.utils import create_secret_key


async def create_url(url: SUrlBase) -> SAddUrl:
    """
     Create a new URL in the database.

     Args:
         url (SUrlBase): The URL to create.

     """
    key_ = await create_unique_random_key()
    secret_key = create_secret_key(key=key_)

    result = await ShortenerRepository.add_url(
        data={
            'target_url': url.target_url,
            'key': key_,
            'secret_key': secret_key,
        }
    )

    base_url = f'{settings().DOMAIN}:{settings().DOMAIN_PORT}'
    result.url = f'{base_url}/{result.key}'

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


async def update_db_clicks(url: SUrlInfo) -> SUrlInfo:
    """
    Update the clicks count for a URL in the database.

    Args:
        url (SUrlInfo): The URL to update.

    Returns:
        Url: The updated URL.
    """
    result = await ShortenerRepository.update_redirect_counter(url)
    return result
