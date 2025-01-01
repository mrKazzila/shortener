import pytest

from app.service_layer.services.urls import UrlsServices


@pytest.mark.integration()
async def test_create_db_url(unit_of_work) -> None:
    """Test the `create_db_url` function."""
    url = "https://leetcode.com/problemset/all/"

    db_url = await UrlsServices.create_url(
        target_url=url,
        uow=unit_of_work,
    )

    assert db_url.target_url == url
    assert db_url.key is not None


@pytest.mark.integration()
async def test_get_db_url_by_key(unit_of_work) -> None:
    """Test the `get_db_url_by_key` function."""
    url = "https://leetcode.com/problemset/all/"

    db_url = await UrlsServices.create_url(
        target_url=url,
        uow=unit_of_work,
    )
    db_url_from_db = await UrlsServices.get_active_long_url_by_key(
        key=db_url.key,
        uow=unit_of_work,
    )

    assert str(db_url_from_db) == str(db_url)
