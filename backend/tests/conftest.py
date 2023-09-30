import asyncio
from typing import AsyncGenerator

import pytest
from app.settings.config import TEST_DB_URL
from app.settings.database import Base, get_async_session
from app.main import app
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.pool import NullPool

test_engine = create_async_engine(
    url=TEST_DB_URL,
    poolclass=NullPool,
)
async_session_maker = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base.metadata.bind = test_engine  # for sync test db with real db


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session
client = TestClient(app)


@pytest.fixture(scope='session')
def event_loop(request):
    """
    This fixture provides a global event loop for all tests in the session.

    Args:
        request: The pytest request object.

    Returns:
        The event loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    """This fixture prepares the database for all tests in the session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """This fixture provides an asynchronous client for all tests in the session."""
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='module')
async def async_session() -> AsyncConnection[AsyncSession, None]:
    """This fixture provides an asynchronous session for all tests in the module."""
    async with async_session_maker() as session:
        yield session
