from app.shortener.keygen import create_unique_random_key
from sqlalchemy.ext.asyncio import AsyncSession


async def test_create_unique_random_key_is_unique(async_session: AsyncSession) -> None:
    """
    Test that create_unique_random_key is unique.

    Args:
         async_session (AsyncSession): The database session.
    """
    key_1 = await create_unique_random_key(session=async_session)
    key_2 = await create_unique_random_key(session=async_session)

    assert key_1 != key_2
