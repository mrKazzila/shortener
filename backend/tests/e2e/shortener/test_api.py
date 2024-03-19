import logging
from http import HTTPStatus
from json import dumps
from typing import Any

import pytest
from httpx import AsyncClient
from tests.e2e.shortener.parametrize_data import (
    post_invalid_data,
    post_valid_data,
)

from schemas.url import SUrl

logger = logging.getLogger(__name__)


@pytest.mark.e2e()
@pytest.mark.parametrize(
    "target_url_",
    post_valid_data,
    ids=str,
)
async def test_create_short_url(
    target_url_: str,
    async_client: AsyncClient,
) -> None:
    """
    Test that a shortened URL can be created successfully.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    response = await async_client.post(
        url="/",
        json={"target_url": target_url_},
    )
    str_data = dumps(response.json())

    assert response.status_code == HTTPStatus.CREATED
    assert SUrl.model_validate_json(str_data)


@pytest.mark.e2e()
@pytest.mark.parametrize(
    "target_url_",
    post_valid_data,
    ids=str,
)
async def test_redirect_to_target_url(
    target_url_: str,
    async_client: AsyncClient,
) -> None:
    """
    Test that redirect by a shortened URL can be successfully.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    response_url = await async_client.post(
        url="/",
        json={"target_url": target_url_},
    )

    data = response_url.json()
    short_url = data.get("url")
    response = await async_client.get(url=short_url)

    assert response.status_code == HTTPStatus.MOVED_PERMANENTLY
    assert response.headers["Location"] == target_url_


@pytest.mark.e2e()
@pytest.mark.parametrize(
    "target_url_",
    post_invalid_data,
    ids=str,
)
async def test_create_short_url_with_invalid_url(
    target_url_: Any,
    async_client: AsyncClient,
) -> None:
    """
    Test that an exception is raised if an invalid URL is provided.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    response = await async_client.post(
        url="/",
        json={"target_url": target_url_},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.e2e()
async def test_redirect_to_target_url_with_invalid_url(
    async_client: AsyncClient,
) -> None:
    """
    Tests that a redirect with invalid URL is failed.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    url_ = "https://www.google.com"

    response_url = await async_client.post(
        url="/",
        json={"target_url": url_},
    )

    data = response_url.json()
    short_url = data.get("url")
    invalid_url = short_url + "t"
    response = await async_client.get(invalid_url)

    assert response.is_success is False
    assert response.headers.get("Location") is None
