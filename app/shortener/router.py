import secrets
from typing import NoReturn

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from validators import url as url_validator

from app.database import get_async_session
from app.shortener.models import Url
from app.shortener.schemas import UrlBase, UrlInfo

router = APIRouter(
    tags=['Shorturl'],
)


def raise_bad_request(message) -> NoReturn:
    raise HTTPException(
        status_code=400,
        detail=message,
    )


@router.post('/url', response_model=UrlInfo)
async def create_url(url: UrlBase, session: AsyncSession = Depends(get_async_session)):
    if not url_validator(url.target_url):
        await raise_bad_request(message='Your provided URL is not valid!')

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))

    db_url = Url(target_url=url.target_url, key=key, secret_key=secret_key)

    session.add(db_url)

    await session.commit()
    await session.refresh(db_url)

    db_url.url = key
    db_url.admin_url = secret_key

    return db_url


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


@router.get("/{url_key}")
async def forward_to_target_url(url_key: str, request: Request, session: AsyncSession = Depends(get_async_session)):
    query = (
        select(Url)
        .filter(Url.key == url_key, Url.is_active)
    )

    result = await session.execute(query)
    row = result.scalar()

    if row:
        return RedirectResponse(row.target_url)
    else:
        raise_not_found(request)
