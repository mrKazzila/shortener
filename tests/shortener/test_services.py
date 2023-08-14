from sqlalchemy.ext.asyncio import AsyncSession

from app.shortener.schemas import UrlBase
from app.shortener.services import (
    create_db_url,
    deactivate_db_url_by_secret_key,
    get_db_url_by_key,
    get_db_url_by_secret_key,
    update_db_clicks,
)


async def test_create_db_url(async_session: AsyncSession) -> None:
    """
    Test the `create_db_url` function.

    Args:
        async_session (AsyncSession): The database session.
    """
    url = UrlBase(target_url='https://leetcode.com/problemset/all/')
    db_url = await create_db_url(session=async_session, url=url)

    assert db_url.target_url == url.target_url
    assert db_url.key is not None
    assert db_url.secret_key is not None


async def test_get_db_url_by_key(async_session: AsyncSession) -> None:
    """
    Test the `get_db_url_by_key` function.

    Args:
        async_session (AsyncSession): The database session.
    """
    db_url = await create_db_url(session=async_session, url=UrlBase(target_url="https://example.com"))
    db_url_from_db = await get_db_url_by_key(session=async_session, url_key=db_url.key)

    assert db_url_from_db == db_url


async def test_get_db_url_by_secret_key(async_session: AsyncSession) -> None:
    """
    Test the `get_db_url_by_secret_key` function.

    Args:
        async_session (AsyncSession): The database session.
    """
    db_url = await create_db_url(session=async_session, url=UrlBase(target_url="https://example.com"))
    db_url_from_db = await get_db_url_by_secret_key(session=async_session, secret_key=db_url.secret_key)

    assert db_url_from_db == db_url


async def test_update_db_clicks(async_session: AsyncSession) -> None:
    """
    Test the `update_db_clicks` function.

    Args:
        async_session (AsyncSession): The database session.
    """
    db_url = await create_db_url(session=async_session, url=UrlBase(target_url="https://example.com"))
    db_url.clicks_count = 0

    await update_db_clicks(session=async_session, db_url=db_url)
    await update_db_clicks(session=async_session, db_url=db_url)

    assert db_url.clicks_count == 2


async def test_deactivate_db_url_by_secret_key(async_session: AsyncSession) -> None:
    """
    Test the `deactivate_db_url_by_secret_key` function.

    Args:
        async_session (AsyncSession): The database session.
    """
    db_url = await create_db_url(session=async_session, url=UrlBase(target_url="https://example.com"))

    assert db_url.is_active is True

    await deactivate_db_url_by_secret_key(session=async_session, secret_key=db_url.secret_key)

    assert db_url.is_active is False
