from fastapi import APIRouter, status

from app.api.routers.healthcheck.data_types import OK_STATUS

router = APIRouter(
    prefix="/api/healthcheck",
    tags=["healthcheck"],
)

__all__ = ("router",)


@router.get(
    path="/",
    name="Simple healthchecker",
    status_code=status.HTTP_200_OK,
)
async def get_status() -> type(OK_STATUS):
    """Returns the health status of the application."""
    return OK_STATUS
