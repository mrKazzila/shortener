import logging
from sys import exit

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.settings.config import settings

logger = logging.getLogger(__name__)


async def redis_setup() -> None:
    """Redis setup."""
    logger.info('Start Redis setup')
    try:
        redis = await aioredis.from_url(
            url=settings().redis_url,
            encoding='utf-8',
            decode_responses=True,
        )

        FastAPICache.init(RedisBackend(redis), prefix='cache')
        logger.info('Redis setup successfully ended')

    except Exception as e:
        logger.error('Redis setup with error: %(error)s', {'error': e})
        exit(e)
