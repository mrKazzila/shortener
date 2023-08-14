from typing import NoReturn

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from validators import url as url_validator

from app.database import get_async_session
from app.shortener.schemas import UrlBase, UrlInfo
from app.shortener.services import create_db_url
from app.shortener.utils import get_db_url_by_key

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
async def create_short_url(url: UrlBase,
                           session: AsyncSession = Depends(get_async_session)
                           ):
    if not url_validator(url.target_url):
        await raise_bad_request(message='Your provided URL is not valid!')

    db_url = await create_db_url(session=session, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key

    return db_url


@router.get("/{url_key}")
async def redirect_to_target_url(url_key: str,
                                 request: Request,
                                 session: AsyncSession = Depends(get_async_session)):
    if db_url := await get_db_url_by_key(session=session, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
