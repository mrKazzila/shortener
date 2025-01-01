from app.api.routers.healthcheck import router as healthcheck_router
from app.api.routers.urls import routers as urls_router

ROUTERS = {healthcheck_router, urls_router}

__all__ = ("ROUTERS",)
