import logging

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from validators import url as url_validator

from app.api.routers.urls._types import PathUrlKey, QueryLongUrl, Uow
from app.api.routers.urls.exceptions import (
    InvalidUrlException,
    UrlNotFoundException,
)
from app.schemas.urls import SReturnUrl
from app.service_layer.services.urls import UrlsServices

__all__ = ("router",)

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["urls"],
)


@router.post(
    path="/",
    name="Create key for short url",
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(
    url: QueryLongUrl,
    uow: Uow,
) -> SReturnUrl:
    """Creates a shortened URL."""
    try:
        if not url_validator(value=str(url)):
            raise InvalidUrlException()

        return await UrlsServices.create_url(
            target_url=url,
            uow=uow,
        )

    except InvalidUrlException as error_:
        logger.error(error_)
        raise error_

    except HTTPException as error_:
        logger.error(error_)
        raise error_


@router.get(
    path="/{url_key}",
    name="Redirect to long url by key",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def redirect_to_target_url(
    url_key: PathUrlKey,
    request: Request,
    uow: Uow,
) -> RedirectResponse:
    """Redirects to the target URL for a given shortened URL key."""
    try:
        db_url = await UrlsServices.get_active_long_url_by_key(
            key=url_key,
            uow=uow,
        )

        if not db_url:
            raise UrlNotFoundException(
                detail=f"{request.url} doesn't exist!",
            )
        _redirect = RedirectResponse(
            url=str(db_url.target_url),
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

        await UrlsServices.update_db_clicks(url=db_url, uow=uow)
        return _redirect

    except UrlNotFoundException as error_:
        logger.error(error_)
        raise error_

    except HTTPException as error_:
        logger.error(error_)
        raise error_
