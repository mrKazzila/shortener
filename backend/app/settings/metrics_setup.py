import logging

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

__all__ = ("metrics_setup",)

logger = logging.getLogger(__name__)


def metrics_setup(*, app: FastAPI) -> None:
    """Setup prometheus fastapi instrumentator for metrics."""
    try:
        __setup(app=app)
    except Exception as error_:
        logger.error(
            "Prometheus fastapi instrumentator setup with error: %s",
            error_,
        )
        exit(error_)


def __setup(*, app: FastAPI) -> None:
    metrics_instrumentator = __prepare_metrics_instrumentator()
    metrics_instrumentator.instrument(app).expose(
        app=app,
        endpoint="/api/metrics",
        tags=["prometheus metrics"],
    )


def __prepare_metrics_instrumentator() -> Instrumentator:
    return Instrumentator(
        should_group_status_codes=False,
        excluded_handlers=["/api/metrics"],
    )
