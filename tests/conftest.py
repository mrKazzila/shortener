import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import TEST_DB_URL
from app.database import get_async_session, metadata
from app.main import app

test_engine = create_async_engine(
    url=TEST_DB_URL,
    poolclass=NullPool,
)
async_session_maker = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
metadata.bind = test_engine


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

client = TestClient(app)


@pytest.fixture(autouse=TEST_DB_URL, scope='session')
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
