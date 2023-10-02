from typing import cast

from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi_cache.decorator import cache
from pydantic import AnyHttpUrl
from validators import url as url_validator

from app.core.exceptions import BadRequestException, UrlNotFoundException
from app.settings.config import settings
from app.shortener import services
from app.shortener.schemas import SUrlBase, SAddUrl

router = APIRouter(
    tags=['ShortUrl'],
)


@router.post(
    path='/',
    name='Create key for short url',
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(url: SUrlBase) -> SAddUrl:
    """
    Creates a shortened URL.

    Args:
        url: The original URL to shorten.

    Returns:
        The shortened URL information.

    Raises:
        ValueError: If the provided URL is not valid.
    """
    if not url_validator(url.target_url):
        raise BadRequestException(detail='Your provided URL is not valid!')

    return await services.create_url(url=url)


@router.get(
    path='/{url_key}',
    name='Redirect to long url by key',
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
@cache(expire=settings().REDIS_CACHE_TIME)
async def redirect_to_target_url(url_key: str, request: Request) -> RedirectResponse:
    """
    Redirects to the target URL for a given shortened URL key.

    Args:
        url_key: The shortened URL key.
        request: The HTTP request object.

    Returns:
        A redirect response to the target URL.

    Raises:
        NotFoundError: If the shortened URL key is not found.
    """
    if db_url := await services.get_active_long_url_by_key(key=url_key):
        await services.update_db_clicks(url=db_url)
        return RedirectResponse(
            url=cast(AnyHttpUrl, db_url.target_url),
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
        )

    url_ = request.url
    raise UrlNotFoundException(detail=f"URL '{url_}' doesn't exist")
