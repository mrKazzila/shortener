import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Request, status
from fastapi.responses import RedirectResponse
from fastapi_cache.decorator import cache
from validators import url as url_validator

from app.core.exceptions import BadRequestException, UrlNotFoundException
from app.core.unit_of_work import UnitOfWork
from app.settings.config import settings
from app.shortener.schemas import SAddUrl, SUrlBase
from app.shortener.services import ShortenerServices

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=['ShortUrl'],
)


@router.post(
    path='/',
    name='Create key for short url',
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(
    url: SUrlBase,
) -> SAddUrl:
    """
    Creates a shortened URL.

    Args:
        url: The original URL to shorten.

    Returns:
        The shortened URL information.

    Raises:
        ValueError: If the provided URL is not valid.
    """
    uow = UnitOfWork()
    target_url = str(url.target_url)

    try:
        if url_validator(value=target_url):
            return await ShortenerServices().create_url(target_url=target_url, uow=uow)

        raise BadRequestException(detail='Your provided URL is not valid!')

    except BadRequestException as err:
        logger.error(err)
    except HTTPException as base_err:
        logger.error('Some problem: %(error)s', {'error': base_err})


@router.get(
    path='/{url_key}',
    name='Redirect to long url by key',
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
@cache(expire=settings().REDIS_CACHE_TIME)
async def redirect_to_target_url(
    url_key: Annotated[str, Path(description='The shortened URL key')],
    request: Request,
) -> RedirectResponse:
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
    uow = UnitOfWork()

    try:
        if db_url := await ShortenerServices().get_active_long_url_by_key(
            key=url_key,
            uow=uow,
        ):
            await ShortenerServices().update_db_clicks(url=db_url, uow=uow)

            return RedirectResponse(
                url=db_url.target_url,
                status_code=status.HTTP_301_MOVED_PERMANENTLY,
            )

        url_ = request.url
        raise UrlNotFoundException(detail=f"URL '{url_}' doesn't exist")

    except UrlNotFoundException as err:
        logger.error(err)
    except HTTPException as base_err:
        logger.error('Some problem %(error)s', {'error': base_err})
