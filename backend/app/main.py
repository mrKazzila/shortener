import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routers_setup
from app.settings.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info("Service started")

    yield
    logger.info("Service exited")


app = FastAPI(
    title="ShortUrl",
    lifespan=lifespan,
)

routers_setup(app=app)

origins = [
    settings().BASE_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Origin",
    ],
)
