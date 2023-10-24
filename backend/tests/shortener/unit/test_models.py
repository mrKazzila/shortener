import pytest
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from app.settings.database import async_session_maker
from app.shortener.models import Url


def __select_by(*, model_params, value: str) -> Select:
    query = (
        select(Url)
        .filter(model_params == value)
    )
    return query


async def test_create_url(async_session: AsyncSession) -> None:
    """
    Test that a URL can be created.

    Args:
         async_session (AsyncSession): The database session.
    """
    url = Url(
        key='foo',
        target_url='https://www.google.com',
    )

    async_session.add(url)
    await async_session.commit()

    assert url in async_session
    assert url.key == 'foo'
    assert url.target_url == 'https://www.google.com'
    assert url.is_active is True
    assert url.clicks_count == 0


async def test_get_url_by_key(async_session: AsyncSession) -> None:
    """
    Test that a URL can be retrieved by its key.

    Args:
         async_session (AsyncSession): The database session.
    """
    url = Url(
        key='foq',
        target_url='https://www.google.com',
    )
    async_session.add(url)
    await async_session.commit()

    query = __select_by(model_params=Url.key, value='foq')
    result = await async_session.execute(query)
    row = result.scalar()
    assert url == row


async def test_update_url(async_session: AsyncSession) -> None:
    """
    Tests that a URL can be updated.

    Args:
         async_session (AsyncSession): The database session.
    """
    url = Url(
        key='fop',
        target_url='https://www.google.com',
    )

    async_session.add(url)
    await async_session.commit()

    url.target_url = 'https://www.zoom.com'
    await async_session.commit()

    query = __select_by(model_params=Url.key, value='fop')
    result = await async_session.execute(query)
    row = result.scalar()

    assert row.target_url == 'https://www.zoom.com'


async def test_create_url_with_invalid_key(async_session: AsyncSession) -> None:
    """
    Tests that a URL cannot be created with an invalid key.

    Args:
         async_session (AsyncSession): The database session.
    """
    with pytest.raises(DBAPIError):
        url = Url(
            key=12345,
            target_url='https://www.google.com',
        )
        async_session.add(url)
        await async_session.commit()


async def test_create_url_with_duplicate_key() -> None:
    """Tests that a URL cannot be created with a duplicate key."""
    async with async_session_maker() as session:
        url1 = Url(
            key='fyn',
            target_url='https://www.google.com',
        )
        session.add(url1)
        await session.commit()

        with pytest.raises(IntegrityError):
            url2 = Url(
                key='fyn',
                target_url='https://www.facebook.com',
            )
            session.add(url2)
            await session.commit()
