from sqlalchemy.ext.asyncio import AsyncSession

import app.shortener.services as services
from app.shortener.utils import generate_random_key


async def create_unique_random_key(session: AsyncSession):
    """
    Creates a unique random key.

    Args:
        session: An asyncio.AsyncSession object.

    Returns:
        A unique random key.
    """
    key = generate_random_key()

    while await services.get_db_url_by_key(session=session, url_key=key):
        key = generate_random_key()

    return key