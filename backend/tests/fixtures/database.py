import pytest

from app.settings.config import settings
from app.settings.database import Base, engine


@pytest.fixture(scope="session", autouse=True)
async def prepare_database() -> None:
    """This fixture prepares the database for all tests in the session."""
    if settings().MODE != "TEST":
        raise Exception(
            "Test must run with TEST mode, but given %{mode}s.",
            {"mode": settings().MODE},
        )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
