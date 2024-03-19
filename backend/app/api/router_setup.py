import logging
from sys import exit

from fastapi import FastAPI

from app.api.healthcheck.routers import router as healthcheck_router
from app.api.urls.routers import router as urls_router

__all__ = ("routers_setup",)

logger = logging.getLogger(__name__)


def routers_setup(app: FastAPI) -> None:
    """Setup project api."""
    try:
        logger.info("Start api setup")

        app.include_router(urls_router)
        app.include_router(healthcheck_router)

        logger.info("Routers setup successfully ended")
    except Exception as error_:
        logger.error(error_)
        exit(error_)
