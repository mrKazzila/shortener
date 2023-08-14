from httpx import AsyncClient


async def test_create_short_url(async_client: AsyncClient) -> None:
    """
    Tests that a shortened URL can be created successfully.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    url = 'https://www.google.com'
    response = await async_client.post(
        '/url',
        json={'target_url': url},
    )

    assert response.status_code == 200

    data = response.json()
    assert data.get('target_url') == url
    assert data.get('is_active')
    assert data.get('clicks_count') == 0
    assert data.get('url') != ''
    assert len(data.get('url')) == 27
    assert data.get('admin_url') != ''
    assert len(data.get('admin_url')) == 42


async def test_create_short_url_with_invalid_url(async_client: AsyncClient) -> None:
    """
    Tests that an exception is raised if an invalid URL is provided.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    url = 'invalid-url'
    response = await async_client.post(
        '/url',
        json={'target_url': url},
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Your provided URL is not valid!'}


async def test_get_url_info(async_client: AsyncClient) -> None:
    """
    Tests that the information for a shortened URL can be retrieved successfully.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    url = 'https://www.google.com'
    response_url = await async_client.post(
        '/url',
        json={'target_url': url},
    )
    create_url = response_url.json()
    secret_key = create_url.get('admin_url')[-14:]

    response_admin_url = await async_client.get(
        f'/admin/{secret_key}',
    )

    assert response_admin_url.status_code == 200

    admin_data = response_admin_url.json()
    assert admin_data == create_url


async def test_get_url_info_with_invalid_secret_key(async_client: AsyncClient) -> None:
    """
    Tests that an exception is raised if an invalid secret key is provided.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    secret_key = 'invalid-secret-key'

    response = await async_client.get(
        f'/admin/{secret_key}',
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "URL 'http://test/admin/invalid-secret-key' doesn't exist"}


async def test_delete_url(async_client: AsyncClient) -> None:
    """
    Tests that a shortened URL can be deleted successfully.

    Args:
         async_client (AsyncClient): The async client obj.
    """

    url = 'https://www.google.com'
    response_url = await async_client.post(
        '/url',
        json={'target_url': url},
    )
    create_url = response_url.json()
    secret_key = create_url.get('admin_url')[-14:]

    response = await async_client.delete(
        f'/admin/{secret_key}',
    )

    assert response.status_code == 200
    assert response.json() == {'detail': f"Successfully deleted shortened URL for '{url}'"}


async def test_delete_url_with_invalid_secret_key(async_client: AsyncClient) -> None:
    """
    Tests that an exception is raised if an invalid secret key is provided.

    Args:
         async_client (AsyncClient): The async client obj.
    """
    secret_key = 'invalid-secret-key'

    response = await async_client.delete(
        f'/admin/{secret_key}',
    )

    assert response.status_code == 404
    assert response.json() == {'detail': "URL 'http://test/admin/invalid-secret-key' doesn't exist"}
