import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings.config import settings
from app.settings.redis_setup import redis_setup
from app.shortener.router import router as shortener_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Service started')
    await redis_setup()
    yield
    logger.info('Service exited')


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
