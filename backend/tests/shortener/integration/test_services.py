import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.shortener.services import ShortenerServices

# TODO: Remove dependencies from the real UoW ???


@pytest.mark.integration
async def test_create_db_url(unit_of_work) -> None:
    """
    Test the `create_db_url` function.

    Args:
        async_session (AsyncSession): The database session.
    """
    url = 'https://leetcode.com/problemset/all/'
    db_url = await ShortenerServices().create_url(target_url=url, uow=unit_of_work)

    assert db_url.target_url == url
    assert db_url.key is not None


@pytest.mark.integration
async def test_get_db_url_by_key(unit_of_work) -> None:
    """
    Test the `get_db_url_by_key` function.

    Args:
        async_session (AsyncSession): The database session.
    """
    url = 'https://leetcode.com/problemset/all/'
    db_url = await ShortenerServices().create_url(target_url=url, uow=unit_of_work)
    db_url_from_db = await ShortenerServices().get_active_long_url_by_key(key=db_url.key, uow=unit_of_work)

    assert str(db_url_from_db) == str(db_url)


# FIXME
@pytest.mark.integration
async def test_update_db_clicks(unit_of_work) -> None:
    """
    Test the `update_db_clicks` function.

    Args:
        async_session (AsyncSession): The database session.
    """
    url = 'https://leetcode.com/problemset/all/'
    db_url = await ShortenerServices().create_url(target_url=url, uow=unit_of_work)
    key = db_url.url

    db_url.clicks_count = 0
    print(db_url.clicks_count)

    await ShortenerServices().update_db_clicks(url=db_url, uow=unit_of_work)
    await ShortenerServices().update_db_clicks(url=db_url, uow=unit_of_work)

    assert db_url.clicks_count == 2
