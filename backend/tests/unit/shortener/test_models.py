import pytest
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from tests.unit.helpers import select_by

from models.urls import Url

from app.settings.database import async_session_maker


async def test_create_url(async_session: AsyncSession) -> None:
    """
    Test that a URL can be created.

    Args:
         async_session (AsyncSession): The database session.
    """
    db_key = "foo"
    target_url = "https://www.google.com"

    url = Url(
        key=db_key,
        target_url=target_url,
    )
    async_session.add(url)
    await async_session.commit()

    assert url in async_session
    assert url.key == db_key
    assert url.target_url == target_url
    assert url.is_active is True
    assert url.clicks_count == 0


async def test_get_url_by_key(async_session: AsyncSession) -> None:
    """
    Test that a URL can be retrieved by its key.

    Args:
         async_session (AsyncSession): The database session.
    """
    db_key = "foq"
    target_url = "https://www.google.com"

    url = Url(
        key=db_key,
        target_url=target_url,
    )
    async_session.add(url)
    await async_session.commit()

    query = select_by(model=Url, model_params=Url.key, value=db_key)
    result = await async_session.execute(query)
    row = result.scalar()

    assert url == row


async def test_update_url(async_session: AsyncSession) -> None:
    """
    Tests that a URL can be updated.

    Args:
         async_session (AsyncSession): The database session.
    """
    db_key = "fop"
    target_url = "https://www.google.com"
    new_target_url = "https://www.zoom.com"

    url = Url(
        key=db_key,
        target_url=target_url,
    )

    async_session.add(url)
    await async_session.commit()

    url.target_url = new_target_url
    await async_session.commit()

    query = select_by(model=Url, model_params=Url.key, value=db_key)
    result = await async_session.execute(query)
    row = result.scalar()

    assert row.target_url == new_target_url


async def test_create_url_with_invalid_key(
    async_session: AsyncSession,
) -> None:
    """
    Tests that a URL cannot be created with an invalid key.

    Args:
         async_session (AsyncSession): The database session.
    """
    with pytest.raises(DBAPIError):
        url = Url(
            key=12345,
            target_url="https://www.google.com",
        )
        async_session.add(url)
        await async_session.commit()


async def test_create_url_with_duplicate_key() -> None:
    """Tests that a URL cannot be created with a duplicate key."""
    db_key = "fyn"
    target_url_1 = "https://www.google.com"
    target_url_2 = "https://www.facebook.com"

    async with async_session_maker() as session:
        url_1 = Url(
            key=db_key,
            target_url=target_url_1,
        )
        session.add(url_1)
        await session.commit()

        with pytest.raises(IntegrityError):
            url_2 = Url(
                key=db_key,
                target_url=target_url_2,
            )
            session.add(url_2)
            await session.commit()
