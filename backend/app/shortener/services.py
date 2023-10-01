from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shortener.keygen import create_unique_random_key
from app.shortener.models import Url
from app.shortener.schemas import SUrl as Url_schema
from app.shortener.schemas import SUrlBase
from app.shortener.utils import create_secret_key


async def create_db_url(session: AsyncSession, url: SUrlBase) -> Url:
    """
     Create a new URL in the database.

     Args:
         session (AsyncSession): The database session.
         url (SUrlBase): The URL to create.

     Returns:
         Url: The newly created URL.
     """
    key = await create_unique_random_key(session=session)
    secret_key = create_secret_key(key=key)

    db_url = Url(
        target_url=url.target_url, key=key, secret_key=secret_key
    )

    session.add(db_url)

    await session.commit()
    await session.refresh(db_url)

    return db_url


async def get_db_url_by_key(session: AsyncSession, url_key: str) -> Url:
    """
    Get a URL from the database by its key.

    Args:
        session (AsyncSession): The database session.
        url_key (str): The key of the URL to get.

    Returns:
        Url: The URL with the given key, or None if it does not exist.
    """
    query = (
        select(Url)
        .filter(Url.key == url_key, Url.is_active)
    )

    result = await session.execute(query)
    row = result.scalar()

    return row


async def get_db_url_by_secret_key(session: AsyncSession, secret_key: str) -> Url:
    """
    Get a URL from the database by its secret key.

    Args:
        session (AsyncSession): The database session.
        secret_key (str): The secret key of the URL to get.

    Returns:
        Url: The URL with the given secret key, or None if it does not exist.
    """
    query = (
        select(Url)
        .filter(Url.secret_key == secret_key, Url.is_active)
    )

    result = await session.execute(query)
    row = result.scalar()

    return row


async def update_db_clicks(session: AsyncSession, db_url: Url_schema) -> Url:
    """
    Update the clicks count for a URL in the database.

    Args:
        session (AsyncSession): The database session.
        db_url (Url_schema): The URL to update.

    Returns:
        Url: The updated URL.
    """
    db_url.clicks_count += 1

    await session.commit()
    await session.refresh(db_url)

    return db_url


async def deactivate_db_url_by_secret_key(session: AsyncSession, secret_key: str) -> Url:
    """
    Set the is_active flag to False for a URL in the database.

    Args:
        session (AsyncSession): The database session.
        secret_key (str): The secret key of the URL to deactivate.

    Returns:
        Url: The deactivated URL.
    """
    db_url = await get_db_url_by_secret_key(session, secret_key)

    if db_url:
        db_url.is_active = False

        await session.commit()
        await session.refresh(db_url)

    return db_url
