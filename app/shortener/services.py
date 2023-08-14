from sqlalchemy.ext.asyncio import AsyncSession

from app.shortener.models import Url
from app.shortener.schemas import UrlBase
from app.shortener.utils import create_unique_random_key, create_secret_key


async def create_db_url(session: AsyncSession, url: UrlBase) -> Url:
    key = await create_unique_random_key(session=session)
    secret_key = create_secret_key(key=key)

    db_url = Url(
        target_url=url.target_url, key=key, secret_key=secret_key
    )

    session.add(db_url)

    await session.commit()
    await session.refresh(db_url)

    return db_url
