from http import HTTPStatus
from json import dumps
from typing import Any

import pytest
from httpx import AsyncClient

from app.shortener.schemas import SAddUrl
from tests.shortener.e2e.parametrize_data import post_valid_data, post_invalid_data


@pytest.mark.e2e
@pytest.mark.parametrize(
    ['target_url_'],
    post_valid_data,
)
async def test_create_short_url(target_url_: str, async_client: AsyncClient) -> None:
    """
    Test that a shortened URL can be created successfully.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    response = await async_client.post(
        url='/',
        json={'target_url': target_url_},
    )
    str_data = dumps(response.json())

    assert response.status_code == HTTPStatus.CREATED
    assert SAddUrl.model_validate_json(str_data)


@pytest.mark.e2e
@pytest.mark.parametrize(
    ['target_url_'],
    post_valid_data,
)
async def test_redirect_to_target_url(target_url_: str, async_client: AsyncClient) -> None:
    """
    Test that redirect by a shortened URL can be successfully.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    response_url = await async_client.post(
        '/',
        json={'target_url': target_url_},
    )

    data = response_url.json()
    short_url = data.get('url')

    response = await async_client.get(url=short_url)

    assert response.status_code == HTTPStatus.MOVED_PERMANENTLY
    assert response.headers["Location"] == target_url_


@pytest.mark.e2e
@pytest.mark.parametrize(
    ['target_url_'],
    post_invalid_data,
)
async def test_create_short_url_with_invalid_url(target_url_: Any, async_client: AsyncClient) -> None:
    """
    Test that an exception is raised if an invalid URL is provided.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    url = 'invalid-url'
    response = await async_client.post(
        '/',
        json={'target_url': url},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    error_msg = response.json().get('detail')[0].get('msg')
    assert error_msg == 'Input should be a valid URL, relative URL without a base'


@pytest.mark.e2e
async def test_redirect_to_target_url_with_invalid_url(async_client: AsyncClient) -> None:
    """
    Tests that a redirect with invalid URL is failed.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    url = 'https://www.google.com'
    response_url = await async_client.post(
        '/',
        json={'target_url': url},
    )

    data = response_url.json()
    short_url = data.get('url')
    invalid_url = short_url + 't'

    response = await async_client.get(invalid_url)

    assert response.is_success is False
    assert response.headers.get("Location") is None