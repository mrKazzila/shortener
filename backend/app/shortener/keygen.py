from sqlalchemy.ext.asyncio import AsyncSession

import app.shortener.services as services
from app.shortener.utils import generate_random_key


async def create_unique_random_key() -> str:
    """
    Creates a unique random key.

    Returns:
        A unique random key.
    """
    key = generate_random_key()

    while await services.get_active_long_url_by_key(key=key):
        key = generate_random_key()

    return key
