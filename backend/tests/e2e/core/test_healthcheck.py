import logging
from http import HTTPStatus

import pytest
from httpx import AsyncClient

logger = logging.getLogger(__name__)


@pytest.mark.e2e
async def test_get_healthcheck_status(async_client: AsyncClient) -> None:
    url_ = '/api/healthcheck/'

    response = await async_client.get(url=url_)
    response_data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_data.get('status') == 'ok'
