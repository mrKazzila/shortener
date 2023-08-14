import secrets
from string import ascii_uppercase, ascii_lowercase, digits

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shortener.models import Url


async def create_unique_random_key(session: AsyncSession):
    key = _generate_random_key()

    while await get_db_url_by_key(session, key):
        key = _generate_random_key()

    return key


async def get_db_url_by_key(session: AsyncSession, url_key: str) -> Url:
    query = (
        select(Url)
        .filter(Url.key == url_key, Url.is_active)
    )

    result = await session.execute(query)
    row = result.scalar()

    return row


def create_secret_key(key):
    return f"{key}_{_generate_random_key(length=8)}"


def _generate_random_key(length: int = 5) -> str:
    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(secrets.choice(chars) for _ in range(length))
