import logging
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings.config import settings
from app.settings.redis_setup import redis_setup
from app.shortener.router import router as shortener_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info('Service started')
    await redis_setup()
    yield
    logger.info('Service exited')


sentry_sdk.init(
    dsn=settings().SENTRY_URL,
    traces_sample_rate=settings().TRACES_SAMPLE_RATE,
    profiles_sample_rate=settings().PROFILES_SAMPLE_RATE,
)

app = FastAPI(lifespan=lifespan)
app.include_router(shortener_router)

origins = [
    settings().BASE_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET', 'POST'],
    allow_headers=[
        'Content-Type',
        'Access-Control-Allow-Origin',
    ],
)
