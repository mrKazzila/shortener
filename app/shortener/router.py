from typing import NoReturn

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import URL
from validators import url as url_validator

from app.config import BASE_URL
from app.database import get_async_session
from app.shortener.models import Url
from app.shortener.schemas import UrlBase, UrlInfo
from app.shortener.services import get_db_url_by_key, create_db_url, get_db_url_by_secret_key, update_db_clicks, \
    deactivate_db_url_by_secret_key

router = APIRouter(
    tags=['Shorturl'],
)


def raise_bad_request(message) -> NoReturn:
    raise HTTPException(
        status_code=400,
        detail=message,
    )


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


@router.post('/url', response_model=UrlInfo)
async def create_short_url(url: UrlBase, session: AsyncSession = Depends(get_async_session)):
    """
    Creates a shortened URL.

    Args:
        url: The original URL to shorten.
        session: An asyncio.AsyncSession object.

    Returns:
        The shortened URL information.

    Raises:
        ValueError: If the provided URL is not valid.
    """
    if not url_validator(url.target_url):
        await raise_bad_request(message='Your provided URL is not valid!')

    db_url = await create_db_url(session=session, url=url)
    url_info = await get_admin_info(db_url=db_url)

    return url_info


@router.get("/{url_key}")
async def redirect_to_target_url(
        url_key: str,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Redirects to the target URL for a given shortened URL key.

    Args:
        url_key: The shortened URL key.
        request: The HTTP request object.
        session: An asyncio.AsyncSession object.

    Returns:
        A redirect response to the target URL.

    Raises:
        NotFoundError: If the shortened URL key is not found.
    """
    if db_url := await get_db_url_by_key(session=session, url_key=url_key):
        await update_db_clicks(session=session, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


@router.get(
    "/admin/{secret_key}",
    name="admin info",
    response_model=UrlInfo,
)
async def get_url_info(
        secret_key: str,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Gets the information for a shortened URL by its secret key.

    Args:
        secret_key: The secret key for the shortened URL.
        request: The HTTP request object.
        session: An asyncio.AsyncSession object.

    Returns:
        The shortened URL information.

    Raises:
        NotFoundError: If the shortened URL secret key is not found.
    """
    if db_url := await get_db_url_by_secret_key(session=session, secret_key=secret_key):
        url_info = await get_admin_info(db_url=db_url)

        return url_info
    else:
        raise_not_found(request)


async def get_admin_info(db_url: Url) -> UrlInfo:
    """
    Gets the admin information for a shortened URL.

    Args:
        db_url: The shortened URL model.

    Returns:
        The shortened URL admin information.
    """
    base_url = URL(BASE_URL)
    admin_endpoint = router.url_path_for(
        "admin info",
        secret_key=db_url.secret_key,
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))

    return db_url


@router.delete("/admin/{secret_key}")
async def delete_url(
        secret_key: str,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Deletes a shortened URL by its secret key.

     Args:
         secret_key: The secret key for the shortened URL.
         request: The HTTP request object.
         session: An asyncio.AsyncSession object.

     Returns:
         A dictionary containing the message that the shortened URL was deleted.

     Raises:
         NotFoundError: If the shortened URL secret key is not found.
     """
    if db_url := await deactivate_db_url_by_secret_key(session=session, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"

        return {"detail": message}
    else:
        raise_not_found(request)
