from asyncio import BaseEventLoop, get_event_loop_policy
from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.main import app as fastapi_app
from app.service_layer.unit_of_work import ABCUnitOfWork, UnitOfWork
from app.settings.database import async_session_maker


@pytest.fixture(scope="session")
def event_loop(request) -> BaseEventLoop:
    """
    This fixture provides a global event loop for all tests in the session.
    """
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    This fixture provides an asynchronous client for all tests in the session.
    """
    async with AsyncClient(
        app=fastapi_app,
        base_url="http://test",
    ) as async_client:
        yield async_client


@pytest.fixture(scope="module")
async def async_session() -> AsyncConnection[AsyncSession, None]:
    """
    This fixture provides an asynchronous session for all tests in the module.
    """
    async with async_session_maker() as async_session:
        yield async_session


@pytest.fixture(scope="module")
def unit_of_work() -> ABCUnitOfWork:
    """
    This fixture provides a real Unit Of Work object
    for all tests in the module.
    """
    return UnitOfWork()
