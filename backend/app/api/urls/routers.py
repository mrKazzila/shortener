import logging
import traceback as tb
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Request, status, Depends
from fastapi.responses import RedirectResponse
from validators import url as url_validator

from routers.exceptions import BadRequestException, UrlNotFoundException
from app.schemas.urls import SUrlBase, SUrl
from service_layer.services.urls import UrlsServices
from service_layer.unit_of_work import ABCUnitOfWork, UnitOfWork

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=['urls'],
)


@router.post(
    path='/',
    name='Create key for short url',
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(
        url: SUrlBase,
        uow: Annotated[type(ABCUnitOfWork), Depends(UnitOfWork)],
) -> SUrl:
    """Creates a shortened URL."""
    target_url = str(url.target_url)

    try:
        if url_validator(value=target_url):
            return await UrlsServices.create_url(
                target_url=target_url,
                uow=uow,
            )

        raise BadRequestException(detail='Your provided URL is not valid!')

    except (BadRequestException, HTTPException) as err:
        trace = tb.format_exception(type(err), err, err.__traceback__)
        logger.error(trace)


@router.get(
    path='/{url_key}',
    name='Redirect to long url by key',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def redirect_to_target_url(
    request: Request,
    url_key: Annotated[str, Path(description='The shortened URL key')],
    uow: Annotated[type(ABCUnitOfWork), Depends(UnitOfWork)],
) -> RedirectResponse:
    """Redirects to the target URL for a given shortened URL key."""

    try:
        if db_url := await UrlsServices.get_active_long_url_by_key(
            key=url_key,
            uow=uow,
        ):
            await UrlsServices.update_db_clicks(url=db_url, uow=uow)

            return RedirectResponse(
                url=db_url.target_url,
                status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            )

        url_ = request.url
        raise UrlNotFoundException(detail=f"URL '{url_}' doesn't exist")

    except (UrlNotFoundException, HTTPException) as err:
        trace = tb.format_exception(type(err), err, err.__traceback__)
        logger.error(trace)
